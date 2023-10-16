/**
 * 整体结构借鉴自 graffiti，在加入更多高级功能前，建议使用 React 重构
 */
import JQueryStatic from 'jquery';
import LoDashStatic from 'lodash';
import {
  markQuizOptionSlots,
  parseQuizOptionSlots,
} from '@boyuai/jupyter-helper/lib/poster-utils';
import { IJupyterCellMetadata } from '@boyuai/jupyter-helper/lib/types';
import { ICell, IJupyter } from './types';
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
import stickerLib from './sticker';

const Jupyter: IJupyter = (window as any)['Jupyter'];

// 利用 ts type 但不引入源码
const $: typeof JQueryStatic = (window as any)['$'];
const _: typeof LoDashStatic = (window as any)['_'];

import '../css/extension.css';

/**
 * 注册博小鱼面板
 */
export const registerBxyPanel = () => {
  bxy.init();
};

const ACTIVATE_BXY_PANEL = '激活博小鱼面板';
const SHOW_BXY_PANEL = '显示博小鱼面板';
const HIDE_BXY_PANEL = '隐藏博小鱼面板';

interface ControlPanelCallback {
  ids: string[];
  event: string;
  fn: () => void;
}

/**
 * 博小鱼面板，用于配置课程单元以及单元步骤。
 */
const bxy: {
  init: () => void;
  initSetupButton: () => void;
  initInteractivity: () => void;
  firstTimeSetup: () => void;
  addEvents: () => void;

  toggleAccessLevel: (level?: AccessLevel) => void;
  changeAccessLevel: (level: AccessLevel) => void;

  panelFadeTime: number;
  sitePanel: JQuery<HTMLElement>;
  outerControlPanel: JQuery<HTMLElement>;
  controlPanelsShell: JQuery<HTMLElement>;
  controlPanelIds: { [key: string]: any };
  setupControlPanels: () => void;
  updateControlPanels: () => void;
  setupOneControlPanel: (
    elemId: string,
    elemHtml: string,
    callbacks?: Array<ControlPanelCallback>
  ) => void;
  bindControlPanelCallbacks: (
    parent: JQuery<HTMLElement>,
    callbacks?: Array<ControlPanelCallback>
  ) => void;
  showControlPanels: (ids: string[]) => void;
  startPanelDragging: (e: any) => void;
  refreshCellSideMarker: (cell: ICell) => void;

  notificationMsgs: { [key: string]: any };
  setNotifier: (msg: string, callbacks?: Array<ControlPanelCallback>) => void;
  resetNotifier: () => void;
} = {
  init: () => {
    console.log('bxy: Main constructor running.');

    const currentAccessLevel = state.getAccessLevel();
    if (currentAccessLevel === 'create') {
      storage.ensureNotebookGetsBxyId();
    }

    bxy.initSetupButton();
    if (Jupyter.notebook.metadata.bxyId) {
      // do not try to load the manifest if this notebook has not yet been bxy-ized.
      storage
        .loadManifest(currentAccessLevel)
        .then(() => {
          bxy.initInteractivity();
        })
        .catch((ex: any) => {
          console.log(
            'bxy: Not setting up bxy because this notebook has never had any authoring done yet (no recordingId).'
          );
          console.log(ex);
        });
    }
  },

  initSetupButton: () => {
    const notebook = Jupyter.notebook;
    // const sprayCanIcon = stickerLib.makeSprayCanIcon();
    const buttonStyleHtml = 'display:none;';
    let buttonLabel,
      setupForSetup = false;
    const buttonContents =
      '<div id="bxy-setup-button" style=' +
      buttonStyleHtml +
      ' class="btn-group"><button class="btn btn-default" title="' +
      '博小鱼面板开关' +
      '">';

    if (!notebook.metadata.bxyId) {
      // This notebook has never been bxy-ized, or it just got un-bxy-ized
      const existingSetupButton = $('#bxy-setup-button');
      if (existingSetupButton.length > 0) {
        existingSetupButton.remove();
      }
      buttonLabel = ACTIVATE_BXY_PANEL;
      setupForSetup = true;
    } else {
      // This notebook has already been bxy-ized. Render the setup button for view mode,
      // which is the default mode to start.
      buttonLabel = SHOW_BXY_PANEL;
    }
    const setupButtonDiv = $(
      buttonContents + '<span>' + buttonLabel + '</div></button></span>'
    );
    const jupyterMainToolbar = $('#maintoolbar-container');
    setupButtonDiv.appendTo(jupyterMainToolbar);
    // $('#bxy-setup-button button').prepend(sprayCanIcon);
    if (setupForSetup) {
      $('#bxy-setup-button').click(() => {
        bxy.firstTimeSetup();
      });
    } else {
      $('#bxy-setup-button').click(() => {
        bxy.toggleAccessLevel();
      });
    }

    $('#bxy-setup-button').show();
  },

  initInteractivity: () => {
    bxy.addEvents();
    bxy.setupControlPanels();
    bxy.updateControlPanels();
    for (const cell of Jupyter.notebook.get_cells()) {
      bxy.refreshCellSideMarker(cell);
    }
  },

  firstTimeSetup: () => {
    storage.ensureNotebookGetsBxyId();
    utils.queueSaveNotebookCallback(() => {
      bxy.initInteractivity();
      bxy.toggleAccessLevel('create');
      $('#bxy-setup-button')
        .unbind('click')
        .click(() => {
          bxy.toggleAccessLevel();
        });
    });
    utils.saveNotebookDebounced();
  },

  addEvents: () => {
    Jupyter.notebook.events.on('select.Cell', (e: any, results: any) => {
      console.log('bxy: cell select event fired, e, cell:', e, results.cell);
      bxy.updateControlPanels();
    });

    Jupyter.notebook.events.on('create.Cell', (e: any, results: any) => {
      // console.log('bxy: cell create event fired, e, cell:', e, results.cell);
      const newCell = results.cell;
      if (utils.getMetadataCellId(newCell.metadata) === undefined) {
        // Do not assign a bxy id if we already have one. This may happen when applyCellListToNotebook is reinserting cells from the history
        // and has set the new cell's id to the value of a historical cell's id.
        utils.setMetadataCellId(newCell.metadata, utils.generateUniqueId());
      } else {
        utils.getMetadataCellId(newCell.metadata);
      }
      utils.refreshCellMaps();
      bxy.updateControlPanels();
    });

    Jupyter.notebook.events.on('delete.Cell', (e: any, results: any) => {
      console.log('bxy: cell delete event fired, e, cell:', e, results.cell);
      utils.refreshCellMaps();
      // 删除后调用 get_selected_cell 会拿到第一个 cell，无法正常更新，所以直接关闭面板
      bxy.toggleAccessLevel('view');
      // bxy.updateControlPanels();
    });

    // Because we get this event when output is sent but before it's rendered into the dom, we set up to collect
    // the output on the next tick rather than this loop.
    Jupyter.notebook.events.on('set_dirty.Notebook', (e: any, results: any) => {
      // console.log('bxy: set_dirty.Notebook, e, results:', e, results);
      utils.refreshCellMaps();
    });

    // 修复了和 graffiti 事件冲突的 bug，可以提个 pr
    window.addEventListener('mousemove', (e) => {
      // console.log('cursorPosition:[',e.clientX, e.clientY, ']');
      // console.log('mouse_e:', e.pageX, e.pageY);
      state.setPointerPosition({ x: e.clientX, y: e.clientY }); // keep track of current pointer position at all times

      let position, newPosition;
      const pointerPosition = state.getPointerPosition();
      const panelBbox = bxy.sitePanel[0].getBoundingClientRect();
      const controlPanelWidth = bxy.outerControlPanel.width()!;
      const controlPanelHeight = bxy.outerControlPanel.height()!;
      const pixelBuffer = 25;
      if (state.getControlPanelDragging()) {
        const offset = state.getControlPanelDragOffset();
        // console.log({ pointerPosition, offset });
        position = {
          x: pointerPosition.x - offset.left,
          y: pointerPosition.y - offset.top,
        };
      }
      if (position !== undefined) {
        // Make sure the control panel stays on screen
        const constrainedLeft = Math.min(
          window.innerWidth - controlPanelWidth - pixelBuffer,
          Math.max(0, position.x)
        );
        const constrainedTop = Math.min(
          panelBbox.bottom - controlPanelHeight - pixelBuffer,
          Math.max(pixelBuffer, position.y)
        );
        // console.log({ constrainedLeft, constrainedTop });

        newPosition = { x: constrainedLeft, y: constrainedTop };
        const newPositionPx = {
          left: newPosition.x + 'px',
          top: newPosition.y + 'px',
          right: 'unset',
        };
        bxy.outerControlPanel.css(newPositionPx);
      }
    });
  },

  changeAccessLevel: (level) => {
    if (level === 'create') {
      storage.ensureNotebookGetsBxyId();
      utils.assignCellIds();
      utils.queueSaveNotebookCallback(() => {
        // bxy.refreshAllBxyHighlights();
        // bxy.refreshBxyTooltipsDebounced();
      });
      utils.saveNotebookDebounced();
    } else {
      bxy.outerControlPanel.fadeOut(bxy.panelFadeTime);
    }
    state.setAccessLevel(level);
    bxy.updateControlPanels();
  },

  toggleAccessLevel: (forcedLevel) => {
    let buttonLabel;
    const level =
      forcedLevel === undefined ? state.getAccessLevel() : forcedLevel;
    if (forcedLevel !== undefined) {
      if (level === 'create') {
        buttonLabel = HIDE_BXY_PANEL;
        bxy.changeAccessLevel('create');
      } else {
        buttonLabel = SHOW_BXY_PANEL;
        bxy.changeAccessLevel('view');
      }
    } else {
      if (level === 'create') {
        buttonLabel = SHOW_BXY_PANEL;
        bxy.changeAccessLevel('view');
      } else {
        buttonLabel = HIDE_BXY_PANEL;
        bxy.changeAccessLevel('create');
      }
    }
    $('#bxy-setup-button span:last').text(buttonLabel);
  },

  panelFadeTime: 350,
  sitePanel: $(),
  outerControlPanel: $(),
  controlPanelsShell: $(),
  controlPanelIds: {},
  setupControlPanels: () => {
    if ($('#bxy-outer-control-panel').length === 0) {
      const outerControlPanel = $(
        '<div id="bxy-outer-control-panel">' +
          '  <div id="bxy-inner-control-panel">' +
          '    <div class="bxy-small-dot-pattern" id="bxy-drag-handle">&nbsp;&nbsp;</div>' +
          '    <div id="bxy-control-panels-shell"></div>' +
          '  </div>' +
          '</div>'
      );
      outerControlPanel.appendTo($('body'));
    }

    bxy.sitePanel = $('#site');
    bxy.outerControlPanel = $('#bxy-outer-control-panel');
    bxy.outerControlPanel.hide();
    bxy.controlPanelsShell = $('#bxy-control-panels-shell');

    const dragHandle = $('#bxy-drag-handle');
    dragHandle
      .on('mousedown', (e) => {
        bxy.startPanelDragging(e);
      })
      .on('mouseup', (e) => {
        if (state.getControlPanelDragging()) {
          console.log('bxy: no longer dragging control panel');
          state.setControlPanelDragging(false);
          e.preventDefault();
          e.stopPropagation();
        }
      });

    const logoText = '博小鱼控制面板';
    bxy.setupOneControlPanel(
      'bxy-control-panel-title',
      '<div>' +
        // stickerLib.makeSmallUdacityIcon({ width: 20, height: 20 }) +
        '</div><div id="bxy-logo-text">' +
        logoText +
        '</div>'
    );

    bxy.setupOneControlPanel('bxy-notifier', '<div />');

    // 在表单使用输入控件时屏蔽快捷键
    const disableJupyterShortcuts = (elem: JQuery<HTMLElement>) => {
      return elem
        .on('focus', () => {
          Jupyter.keyboard_manager.disable();
        })
        .on('blur', () => {
          Jupyter.keyboard_manager.enable();
        });
    };
    const makeFormItem = (elemId: string, label: string) => {
      const fullHtml =
        '<div class="bxy-form-item" id="' +
        elemId +
        `"><span style="flex: 1;text-align-last: justify;">${label}</span></div>`;
      return $(fullHtml);
    };

    bxy.setupOneControlPanel(
      'bxy-lesson-config',
      '<div class="bxy-config-title">单元配置</div>'
    );

    const posterTemplateItem = makeFormItem(
      'poster-template-item',
      '海报模板ID'
    );
    $('#bxy-lesson-config').append(posterTemplateItem);
    const posterTemplateInput = disableJupyterShortcuts(
      $('<input style="width: 130px;" />')
        .attr('type', 'text')
        .on('input', (events) => {
          const posterId = (events.target as HTMLInputElement).value;
          if (posterId) {
            Jupyter.notebook.metadata.bxyPosterId = posterId;
          } else {
            delete Jupyter.notebook.metadata.bxyPosterId;
          }
        })
    );
    $('#poster-template-item').append(posterTemplateInput);

    bxy.setupOneControlPanel(
      'bxy-cell-config',
      '<div class="bxy-config-title">Cell配置</div>'
    );

    const posterSlotItem = makeFormItem('poster-slot-item', '海报素材占位ID');
    $('#bxy-cell-config').append(posterSlotItem);
    const posterSlotInput = disableJupyterShortcuts(
      $('<input style="width: 100px;" />')
        .attr('type', 'text')
        .on('input', (events) => {
          const posterSlotId = (events.target as HTMLInputElement).value;
          const activeCell = Jupyter.notebook.get_selected_cell();
          if (posterSlotId) {
            activeCell.metadata.bxyPosterSlotId = posterSlotId;
          } else {
            delete activeCell.metadata.bxyPosterSlotId;
          }
        })
    );
    $('#poster-slot-item').append(posterSlotInput);

    const posterQuizOptionItem = makeFormItem(
      'poster-quiz-option-item',
      '海报Quiz占位ID'
    );
    $('#bxy-cell-config').append(posterQuizOptionItem);
    const posterQuizOptionInput = disableJupyterShortcuts(
      $('<input style="width: 100px;" />')
        .attr('type', 'text')
        .on('input', (events) => {
          bxy.resetNotifier();
          state.formHasError = false;
          const posterQuizOptId = (events.target as HTMLInputElement).value;
          const activeCell = Jupyter.notebook.get_selected_cell();
          try {
            activeCell.metadata = markQuizOptionSlots(
              activeCell.metadata,
              posterQuizOptId
            );
          } catch (err) {
            bxy.setNotifier(err?.message || '未知错误');
            state.formHasError = true;
          }
        })
    );
    $('#poster-quiz-option-item').append(posterQuizOptionInput);

    bxy.setupOneControlPanel('bxy-config-btns', '');
    const save = () => {
      utils.saveNotebookDebounced();
      const activeCell = Jupyter.notebook.get_selected_cell();
      bxy.refreshCellSideMarker(activeCell);
      alert('保存成功');
    };
    const saveBtn = $('<button class="bxy-save-btn">保存</button>').on(
      'click',
      () => {
        if (state.formHasError) {
          alert('请先改正配置');
          return;
        }
        save();
      }
    );
    const saveAndCloseBtn = $(
      '<button class="bxy-close-btn">保存并关闭</button>'
    ).on('click', () => {
      if (state.formHasError) {
        alert('请先改正配置');
        return;
      }
      save();
      bxy.toggleAccessLevel('view');
    });
    $('#bxy-config-btns').append(saveBtn);
    $('#bxy-config-btns').append(saveAndCloseBtn);
  },
  updateControlPanels: () => {
    const accessLevel = state.getAccessLevel();
    const outerControlHidden = bxy.outerControlPanel.css('display') === 'none';
    if (accessLevel === 'create') {
      if (outerControlHidden) {
        // fadeins/fadeouts cause race conditions when you interrupt a movie in progress
        bxy.outerControlPanel.fadeIn(bxy.panelFadeTime);
        // bxy.outerControlPanel.show();
      }
    }

    // 我们没有太多的状态，直接使用 idle 模式
    const visibleControlPanels = [
      'bxy-notifier',
      'bxy-lesson-config',
      'bxy-cell-config',
      'bxy-config-btns',
    ];

    bxy.resetNotifier();

    // 读取 metadata
    const posterId = Jupyter.notebook.metadata.bxyPosterId;
    $('#poster-template-item input').val(posterId || '');
    const activeCellMetadata = Jupyter.notebook.get_selected_cell().metadata;
    const posterSlotId = activeCellMetadata.bxyPosterSlotId;
    const posterQuizOptId = parseQuizOptionSlots(activeCellMetadata);
    $('#poster-slot-item input').val(posterSlotId || '');
    $('#poster-quiz-option-item input').val(posterQuizOptId || '');
    bxy.showControlPanels(visibleControlPanels);
  },
  showControlPanels: (panels) => {
    bxy.controlPanelsShell.children().hide();
    bxy.controlPanelIds['bxy-control-panel-title'].css({
      display: 'flex',
    }); // the title bar is always shown
    for (const controlPanelId of panels) {
      // console.log('bxy: showing panel:', controlPanelId);
      bxy.controlPanelIds[controlPanelId].show();
    }
  },
  /**
   * 注册面板组件
   */
  setupOneControlPanel: (elemId, elemHtml, callbacks) => {
    if (bxy.controlPanelIds === undefined) {
      bxy.controlPanelIds = {};
    }
    const fullHtml =
      '<div class="bxy-control-panel" id="' +
      elemId +
      '">' +
      elemHtml +
      '</div>';
    const elem = $(fullHtml);
    elem.appendTo(bxy.controlPanelsShell);
    bxy.controlPanelIds[elemId] = bxy.controlPanelsShell.find('#' + elemId);
    bxy.bindControlPanelCallbacks(bxy.controlPanelIds[elemId], callbacks);
  },
  bindControlPanelCallbacks: (parent, callbacks) => {
    if (callbacks !== undefined) {
      let cb, id;
      for (cb of callbacks) {
        for (id of cb.ids) {
          parent.find('#' + id).on(cb.event, cb.fn);
        }
      }
    }
  },
  startPanelDragging: (e) => {
    console.log('bxy: dragging control panel');
    const controlPanelPosition = bxy.outerControlPanel.position();
    const pointerPosition = state.getPointerPosition();
    state.setControlPanelDragging(true);
    state.setControlPanelDragOffset({
      left: pointerPosition.x - controlPanelPosition.left,
      top: pointerPosition.y - controlPanelPosition.top,
    });
    e.preventDefault();
    e.stopPropagation();
  },
  refreshCellSideMarker: (cell: ICell) => {
    const element = $(cell.element[0]);
    element
      .find('.bxy-right-side-marker')
      .unbind('mouseenter mouseleave click')
      .remove(); // remove all previous markers for this cell
    if (!cell.metadata.bxyCellId) {
      return;
    }
    if (
      Object.keys(cell.metadata).filter((key) => key.startsWith('bxy'))
        .length <= 1
    ) {
      return;
    }
    const markerIcon = stickerLib.makeRightSideMarker({
      color: '#ffc963',
      dimensions: {
        x: element.width()! + 12,
        y: 10,
        width: 18,
        height: 12,
      },
      metaTag: 'bxy-id|' + cell.metadata.bxyCellId,
      title: 'Cell 含有博小鱼特殊配置',
    });
    $(markerIcon).appendTo(element);
    const markerIcons = element.find('.bxy-right-side-marker');
    if (markerIcons.length > 0) {
      markerIcons.on('click', () => {
        bxy.toggleAccessLevel('create');
      });
    }
  },

  notificationMsgs: {},
  setNotifier: (notificationMsg, callbacks) => {
    const notifierPanel = bxy.controlPanelIds['bxy-notifier'];
    notifierPanel.show().children().hide();
    if (!bxy.notificationMsgs.hasOwnProperty(notificationMsg)) {
      const notificationId = 'bxy-notification-' + utils.generateUniqueId();
      const notificationHtml = $(
        '<div id="' + notificationId + '">' + notificationMsg + '</div>'
      );
      notificationHtml.appendTo(notifierPanel);
      const newNotificationDiv = notifierPanel.find('#' + notificationId);
      bxy.notificationMsgs[notificationMsg] = newNotificationDiv;
      bxy.bindControlPanelCallbacks(newNotificationDiv, callbacks);
    }
    bxy.notificationMsgs[notificationMsg].show();
  },
  resetNotifier: () => {
    bxy.setNotifier(
      '<div>' +
        '<a target="_blank" href="https://fe9m1yda6v.feishu.cn/docs/doccnQKBB3HazZtDhZYcHaunUte">使用说明</a>' +
        '</div>'
    );
  },
};

type AccessLevel = 'create' | 'view';
type Manifest = { [key: string]: any };
type DragOffset = { left: number; top: number };
type PointerPos = { x: number; y: number };

const state: {
  accessLevel: AccessLevel;
  getAccessLevel: () => AccessLevel;
  setAccessLevel: (level: AccessLevel) => void;

  manifest: Manifest; // TODO: 完善类型定义
  getManifest: () => Manifest;

  controlPanelDragging: boolean;
  getControlPanelDragging: () => boolean;
  setControlPanelDragging: (dragging: boolean) => void;
  controlPanelDragOffset: DragOffset;
  getControlPanelDragOffset: () => DragOffset;
  setControlPanelDragOffset: (offset: DragOffset) => void;

  pointer: PointerPos;
  getPointerPosition: () => PointerPos;
  setPointerPosition: (pp: PointerPos) => void;

  formHasError: boolean;

  // cellIdToBxyMap: { [key: string]: any }; // TODO: 完善类型定义
  // refreshCellIdToBxyMap: () => void;
} = {
  formHasError: false,
  accessLevel: 'view',
  getAccessLevel: () => state.accessLevel,
  setAccessLevel: (level) => (state.accessLevel = level),

  manifest: {},
  getManifest: () => {
    return state.manifest;
  },

  controlPanelDragging: false,
  getControlPanelDragging: () => {
    return state.controlPanelDragging;
  },
  setControlPanelDragging: (dragging) => {
    state.controlPanelDragging = dragging;
  },
  controlPanelDragOffset: { left: 0, top: 0 },
  getControlPanelDragOffset: () => {
    return state.controlPanelDragOffset;
  },
  setControlPanelDragOffset: (offset) => {
    state.controlPanelDragOffset = offset;
  },

  pointer: { x: 0, y: 0 },
  getPointerPosition: () => {
    return state.pointer;
  },
  setPointerPosition: (pp) => {
    state.pointer = pp;
  },

  // cellIdToBxyMap: {},
  // refreshCellIdToBxyMap: () => {
  //   state.cellIdToBxyMap = {};
  //   const manifest = state.getManifest();
  //   let recording, recordingCellId, recordingKeys, i, saveToFileEntry, cellId;
  //   for (recordingCellId of Object.keys(manifest)) {
  //     recordingKeys = Object.keys(manifest[recordingCellId]);
  //     for (const recordingKey of recordingKeys) {
  //       recording = manifest[recordingCellId][recordingKey];
  //       if (
  //         recording.saveToFile !== undefined &&
  //         recording.saveToFile.length > 0
  //       ) {
  //         for (i = 0; i < recording.saveToFile.length; ++i) {
  //           saveToFileEntry = recording.saveToFile[i];
  //           cellId = saveToFileEntry.cellId;
  //           if (state.cellIdToBxyMap[cellId] === undefined) {
  //             state.cellIdToBxyMap[cellId] = [];
  //           }
  //           state.cellIdToBxyMap[cellId].push(saveToFileEntry.path);
  //         }
  //       }
  //     }
  //   }
  //   //console.log('bxy: cellIdToBxyMap:', state.cellIdToBxyMap);
  // },
};

const storage = {
  ensureNotebookGetsBxyId: () => {
    // Make sure a new notebook gets a recording id
    const notebook = Jupyter.notebook;
    if (!notebook.metadata.bxyId) {
      notebook.metadata.bxyId = utils.generateUniqueId();
    }
    utils.assignCellIds();
    utils.refreshCellMaps();
    console.log('bxy: Notebook is now ready to use bxy.');
  },

  // Load the manifest for this notebook.
  // Manifests contain information about all the recordings present in this notebook.
  // This version of the system only supports author manifests.
  loadManifest: (currentAccessLevel: AccessLevel) => {
    const notebook = Jupyter.notebook;
    if (!notebook.metadata.bxyId) {
      if (currentAccessLevel !== 'create') {
        console.log(
          'bxy: loadManifest is bailing early because we are not in "create" mode and this notebook has no bxy id.'
        );
        return Promise.reject();
      } else {
        storage.ensureNotebookGetsBxyId();
      }
    }

    // 暂不引入 manifest 文件存储概念
    return Promise.resolve();
  },
};

const utils: {
  saveNotebookCallbacks: (() => void)[];
  queueSaveNotebookCallback: (cb: () => void) => void;

  generateUniqueId: () => string;
  assignCellIds: () => void;
  getMetadataCellId: (metadata: IJupyterCellMetadata) => string | undefined;
  setMetadataCellId: (metadata: IJupyterCellMetadata, cellId: string) => string;

  processSaveNotebookCallbacks: () => void;
  saveNotebook: () => void;
  saveDebounceTiming: number;
  saveNotebookDebounced: () => void;

  cellMaps: { [key: string]: any }; // TODO: 完善类型定义
  refreshCellMaps: () => void;

  createBxyTagRegex: () => RegExp;
} = {
  saveNotebookCallbacks: [],
  queueSaveNotebookCallback: (cb) => {
    utils.saveNotebookCallbacks.push(cb);
  },

  generateUniqueId: () => {
    return 'id_' + Math.random().toString(36).substr(2, 7);
  },
  // Assign cellIds to any cells that don't have them yet.
  assignCellIds: () => {
    const cells = Jupyter.notebook.get_cells();
    let cell, cellId;
    for (let i = 0; i < cells.length; ++i) {
      cell = cells[i];
      cellId = utils.generateUniqueId();
      if (utils.getMetadataCellId(cell.metadata) === undefined) {
        utils.setMetadataCellId(cell.metadata, cellId);
      }
    }
  },
  // These two functions help us translate between what we store in the notebook json itself ('bxyCellId') and how we use it in the code, just as 'cellId'.
  // This was done to make our tags less likely to collide with other Jupyter plugins, but we wanted to keep the field name short in the bxy code.
  getMetadataCellId: (metadata) => {
    return metadata.bxyCellId;
  },
  setMetadataCellId: (metadata, cellId) => {
    metadata.bxyCellId = cellId;
    return cellId;
  },

  processSaveNotebookCallbacks: () => {
    let cb;
    while (utils.saveNotebookCallbacks.length > 0) {
      cb = utils.saveNotebookCallbacks.shift();
      cb?.();
    }
    console.log('bxy: Notebook saved successfully.');
  },
  saveNotebook: () => {
    Jupyter.notebook
      .save_notebook()
      .then(() => {
        utils.processSaveNotebookCallbacks();
      })
      .catch((ex: any) => {
        console.error('bxy: saveNotebook caught exception:', ex);
      });
  },
  saveDebounceTiming: 1000, // Must be slower than 500ms, which is the speed at which jupyter traps save calls stepping on each other. See:
  // https://github.com/jupyter/notebook/blob/859ae0ac60456c0e38b44f06852b8a24f8a1cfb0/notebook/static/notebook/js/notebook.js#L2766
  saveNotebookDebounced: () => {
    _.debounce(utils.saveNotebook, utils.saveDebounceTiming)();
  },

  createBxyTagRegex: () => {
    return RegExp('<span class="bxy-highlight (bxy-[^"]+)">(.*?)</span>', 'gm');
  },
  cellMaps: {},
  // Also note any bxys present in this cell, if it is a markdown cell, so that we can process their removal correctly if the user
  // has moved them from where they were created originally (for instance, bxy buttons).
  refreshCellMaps: () => {
    utils.cellMaps = {
      cells: Jupyter.notebook.get_cells(),
      maps: {},
      location: {}, // the id of the cell every bxy is actually currently located in (may not be the cell where it was created)
    };
    let cell, cellId, cellDOM, tagsRe, bxyId;
    const cellKeys = Object.keys(utils.cellMaps.cells);
    for (let cellIndex = 0; cellIndex < cellKeys.length; ++cellIndex) {
      cell = utils.cellMaps.cells[cellIndex];
      cellId = utils.getMetadataCellId(cell.metadata);
      // Support lookups by cellId.
      utils.cellMaps.maps[cellId!] = cellIndex;
      // Dress up the DOM  cellId so we can track selections in them (pretty much only markdown, selections in code_mirror are done through its API
      if (cell.hasOwnProperty('inner_cell')) {
        cellDOM = $(cell.inner_cell).parents('.cell');
      } else if (cell.hasOwnProperty('element')) {
        cellDOM = $(cell.element);
      }
      if (cellDOM !== undefined) {
        cellDOM.attr({
          'bxy-cell-id': utils.getMetadataCellId(cell.metadata),
        });
      }
      if (cell.cell_type === 'markdown') {
        const contents = cell.get_text();
        tagsRe = utils.createBxyTagRegex();
        let match, idMatch;
        while ((match = tagsRe.exec(contents)) !== null) {
          idMatch = match[1].match(/bxy-(id_.[^-]+)-(id_[^\s]+)/);
          bxyId = idMatch?.[1] + '_' + idMatch?.[2];
          utils.cellMaps.location[bxyId] = cellId;
        }
      }
      // console.trace('cellMaps',utils.cellMaps.location);
    }
  },
};
