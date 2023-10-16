// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

import { registerBbyButtons, workRegx } from './buttons';
import { registerBxyPanel } from './panel';

// Entry point for the notebook bundle containing custom model definitions.
//
// Setup notebook base URL
//
// Some static assets may be required by the custom widget javascript. The base
// url for the notebook is not known at build time and is therefore computed
// dynamically.
(window as any).__webpack_public_path__ =
  // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
  document.querySelector('body')!.getAttribute('data-base-url') +
  'nbextensions/ipybbycell';

// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
define(['base/js/namespace', 'jquery'], (Jupyter, $) => {
  'use strict';

  (window as any)['requirejs'].config({
    map: {
      '*': {
        ipybbycell: 'nbextensions/ipybbycell/extension',
      },
    },
  });

  function registerHelpMenuItem() {
    if ($('#jupyter_bby_help').length > 0) {
      return;
    }
    const menu_item = $('<li/>').append(
      $('<a/>')
        .html('博小鱼文档')
        .attr('title', '博小鱼文档')
        .attr('id', 'jupyter_bby_help')
        .attr(
          'href',
          'https://fe9m1yda6v.feishu.cn/docs/doccnfjrG2MKIq7echn96kyuakc'
        )
        .attr('target', '_blank')
        .append($('<i/>').addClass('fa fa-external-link menu-icon pull-right'))
    );
    menu_item.insertBefore($($('#help_menu > .divider')[1]));
  }

  // Export the required load_ipython_extension function
  function load_ipython_extension() {
    if (
      workRegx.test(Jupyter.notebook.notebook_path) ||
      location.host.includes('localhost')
    ) {
      console.log('Current namespace:', Jupyter);
      registerBbyButtons();
      registerHelpMenuItem();
      registerBxyPanel();
    }
  }
  return {
    load_ipython_extension,
  };
});
