import React from 'react';
import { Row, Col } from 'react-bootstrap';
import { useSelector } from 'react-redux';
import { RootState } from '../../redux/store';
import TimeDropDown from '../components/buttons/TimeDropDown';
import CodeExecComponent from '../components/notebook/CodeExecComponent';
import TimeSpentComponent from '../components/notebook/TimeSpentComponent';
import { NotebookCell } from '../../redux/types';

interface INotebookPageProps {
  notebookId: string;
  notebookName: string;
}

export interface IChartProps {
  notebookId: string;
  timeWindow: string;
  refreshRequired: boolean;
  notebookCells: NotebookCell[] | null;
}

const Notebook = (props: INotebookPageProps): JSX.Element => {
  const timeWindow = useSelector(
    (state: RootState) => state.commondashboard.timeWindow
  );
  const refreshRequired = useSelector(
    (state: RootState) => state.commondashboard.refreshBoolean
  );
  const notebookCells = useSelector(
    (state: RootState) => state.commondashboard.notebookCells
  );

  return (
    <>
      <div className="dashboard-title-container">
        <div className="dashboard-title-text">{props.notebookName}</div>
        <div className="dashboard-dropdown-container">
          <TimeDropDown />
        </div>
      </div>
      <Row>
        <Col>
          <CodeExecComponent
            notebookId={props.notebookId}
            timeWindow={timeWindow}
            refreshRequired={refreshRequired}
            notebookCells={notebookCells}
          />

          <TimeSpentComponent
            notebookId={props.notebookId}
            timeWindow={timeWindow}
            refreshRequired={refreshRequired}
            notebookCells={notebookCells}
          />
        </Col>
      </Row>
    </>
  );
};

export default Notebook;
