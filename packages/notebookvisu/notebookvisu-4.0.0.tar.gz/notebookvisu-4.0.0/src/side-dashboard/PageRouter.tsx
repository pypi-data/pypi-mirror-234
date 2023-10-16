import React from 'react';
import TopBreadcrumb from './components/layout/TopBreadcrumb';
import Notebook from './pages/Notebook';
import Cell from './pages/Cell';

import { useSelector } from 'react-redux';
import { RootState } from '../redux/store';
import { IMarkdownTranslator } from '../plugins/sideDashboard';

// register needed for react-chartjs-2 to work
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);

interface IRouterProps {
  notebookId: string;
  notebookName: string;
  markdownTranslator: IMarkdownTranslator;
}

const PageRouter = (props: IRouterProps): JSX.Element => {
  // state for conditional rendering
  const navigationState = useSelector(
    (state: RootState) => state.sidedashboard.navigationState
  );

  ////////////////////////////////////////////////////////////////

  return (
    <div className="page-container">
      <TopBreadcrumb />
      {/* immediately invoked function expression (IIFE) : */}
      {(() => {
        const currentPage = navigationState[navigationState.length - 1];
        switch (currentPage.pageName) {
          case 'Notebook':
            return (
              <Notebook
                notebookId={props.notebookId}
                notebookName={props.notebookName}
              />
            );
          case 'Cell':
            return (
              <Cell
                notebookId={props.notebookId}
                markdownTranslator={props.markdownTranslator}
              />
            );
          default:
            return null;
        }
      })()}
    </div>
  );
};

export default PageRouter;
