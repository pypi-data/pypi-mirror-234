import type {
  IJupyterCell,
  IJupyterMetadata,
  IJupyterCellMetadata,
} from '@boyuai/jupyter-helper/lib/types';

export interface ICell
  extends Omit<IJupyterCell, '$cellIndex' | 'dryrunOutputs'> {
  metadata: IJupyterCellMetadata;
  execution_count: number | null;
  element: HTMLElement[];
  get_text: () => string;
  set_text: any;
}

export interface IJupyterNotebook {
  metadata: IJupyterMetadata;
  base_url: string;
  notebook_path: string;
  events: any;
  get_cell: (index: number) => ICell;
  get_cells: () => ICell[];
  get_selected_cell: () => ICell;
  get_selected_index: () => number | null;
  focus_cell: () => void;
  select: (index: number) => any;
  insert_cell_below: (type: 'code' | 'markdown') => any;
  delete_cells: () => void;
  toJSON: () => Record<string, any>;
  save_notebook: () => Promise<any>;
}

export interface IJupyter {
  notebook: IJupyterNotebook;
  toolbar: any;
  keyboard_manager: any;
  dialog: {
    modal: (options: {
      title: string;
      body: string;
      sanitize?: boolean;
      buttons?: Record<string, any>;
    }) => any; // https://github.com/jupyter/notebook/blob/master/notebook/static/base/js/dialog.js#L40
  };
}
