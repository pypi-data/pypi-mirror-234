import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';
import { IThemeManager } from '@jupyterlab/apputils';
import { INotebookTracker, NotebookActions } from '@jupyterlab/notebook';
import { ISettingRegistry } from '@jupyterlab/settingregistry';

/**
 * A plugin that sends notebook events to Fusion.
 */
export const cogniteMetrics: JupyterFrontEndPlugin<void> = {
  id: 'cognite_jupyterlab_metrics:plugin',
  autoStart: true,
  requires: [INotebookTracker, IThemeManager],
  optional: [ISettingRegistry],
  activate: (
    app: JupyterFrontEnd,
    nbTracker: INotebookTracker,
    manager: IThemeManager,
    settingRegistry: ISettingRegistry | null
  ) => {
    // Try to read the settings so that the cell toolbar updates
    if (settingRegistry) {
      void settingRegistry.load('@jupyterlab/comments-extension:notebook');
    }

    const executedCode: { [key: string]: string[] } = {};
    let currentNotebook: string | undefined = undefined;

    const track = (eventName: string, data: any) => {
      window.parent.postMessage(
        {
          event: 'jupyterliteEvent',
          data: { eventName, data }
        },
        '*'
      );
    };

    (window as any).nbTracker = nbTracker;
    nbTracker.currentChanged.connect((sender, notebook) => {
      const notebookTitle = (notebook?.context as any)._path;
      currentNotebook = notebookTitle;
      track('jupyterLiteNotebookChanged', { notebookTitle });
    });

    nbTracker.activeCellChanged.connect((sender, cell) => {
      track('jupyterLiteActiveCellChanged', {});
    });

    NotebookActions.executed.connect((sender, args) => {
      const { cell } = args;

      // console.log('Cell: ', cell);
      (window as any).cell = cell;
      const cellModel: any = cell.model.toJSON();
      (window as any).cellModel = cellModel;
      console.log('Cell model: ', cellModel);

      const executionCount = cellModel.execution_count;
      const code = cellModel.source;
      const cellType = cellModel.cell_type;
      const outputs = cellModel.outputs;
      const anyErrors = outputs.some(
        (output: any) => output.output_type === 'error'
      );

      if (currentNotebook === undefined) {
        return;
      }

      if (executedCode[currentNotebook] === undefined) {
        executedCode[currentNotebook] = [];
      }
      executedCode[currentNotebook].push(code);

      track('jupyterLiteCellExecuted', {
        cellType,
        executionCount,
        code,
        success: !anyErrors
      });

      if (anyErrors) {
        const errorOutput = outputs.find(
          (output: any) => output.output_type === 'error'
        );
        const errorName = errorOutput.ename;
        const errorValue = errorOutput.evalue;
        const errorTraceback = errorOutput.traceback.join('\n');

        track('jupyterLiteCellError', {
          cellType,
          executionCount,
          code,
          errorName,
          errorValue,
          errorTraceback,
          executedCode: executedCode[currentNotebook]
        });
      }
    });
  }
};

export default cogniteMetrics;
