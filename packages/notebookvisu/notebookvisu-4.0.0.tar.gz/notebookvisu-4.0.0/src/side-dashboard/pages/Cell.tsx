import React, { useState, useEffect } from 'react';
import {
  Row,
  Col,
  Card,
  Form,
  ToggleButton,
  ButtonGroup
} from 'react-bootstrap';
import { BACKEND_API_URL } from '../../utils/constants';

import { useSelector } from 'react-redux';
import { RootState } from '../../redux/store';
import { CellLayer } from '../../redux/types';
import Loader from '../components/placeholder/Loader';
import CellOutput from '../components/cell/CellOutput';
import CellInput from '../components/cell/CellInput';
import TimeDropDown from '../components/buttons/TimeDropDown';
import SortDropDown from '../components/buttons/SortDropDown';

import MarkdownComponent from '../components/cell/MarkdownComponent';
import { IMarkdownTranslator } from '../../plugins/sideDashboard';

interface ICellPageProps {
  notebookId: string;
  markdownTranslator: IMarkdownTranslator;
}

const Cell = (props: ICellPageProps): JSX.Element => {
  const [apiData, setApiData] = useState([]);
  // for the Loader rendering
  const [isFetching, setIsFetching] = useState(false);
  // declaring a 2nd boolean since state updates are async, which wouldn't be quick enough for the 2nd useEffect check
  let isAlreadyFetching = false;

  const navigationState = useSelector(
    (state: RootState) => state.sidedashboard.navigationState
  );
  const timeWindow = useSelector(
    (state: RootState) => state.commondashboard.timeWindow
  );
  const refreshRequired = useSelector(
    (state: RootState) => state.commondashboard.refreshBoolean
  );

  // filter header content

  const [showInputs, setShowInputs] = useState<boolean>(true);
  const [showOutputs, setShowOutputs] = useState<boolean>(true);

  const [radioValue, setRadioValue] = useState<number>(1);

  const executionFilters = [
    { name: 'All', value: 1, status: 'all' },
    { name: 'Successfully Executed', value: 2, status: 'ok' },
    { name: 'Error', value: 3, status: 'error' }
  ];
  const filterStatus = executionFilters.map(filter => filter.status);

  const [orderBy, setOrderBy] = useState<string>('timeDesc'); // timeDesc (default), timeAsc, inputDesc, inputAsc, outputDesc, outputAsc

  // sorting

  const orderAndSetData = (data: any): void => {
    data.sort((a: any, b: any) => {
      switch (orderBy) {
        case 'timeDesc':
          return new Date(a.t_finish) < new Date(b.t_finish) ? 1 : -1;
        case 'timeAsc':
          return new Date(a.t_finish) > new Date(b.t_finish) ? 1 : -1;
        case 'inputAsc':
          return a.cell_input.length - b.cell_input.length;
        case 'inputDesc':
          return b.cell_input.length - a.cell_input.length;
        case 'outputAsc':
          return a.cell_output_length - b.cell_output_length;
        case 'outputDesc':
          return b.cell_output_length - a.cell_output_length;
        default:
          return 0;
      }
    });
    setApiData(data);
  };

  // fetching

  const content = (navigationState[navigationState.length - 1] as CellLayer)
    .content;

  useEffect(() => {
    setIsFetching(true);
    isAlreadyFetching = true;
    fetch(
      `${BACKEND_API_URL}/dashboard/${props.notebookId}/cell/${content.cellId}?timeWindow=${timeWindow}`
    )
      .then(response => response.json())
      .then(data => {
        orderAndSetData(data);
        setIsFetching(false);
        isAlreadyFetching = false;
      });
  }, [navigationState, timeWindow, refreshRequired]);

  useEffect(() => {
    if (!isAlreadyFetching) {
      // to avoid sorting twice upon first render
      const data = [...apiData];
      orderAndSetData(data);
    }
  }, [orderBy]);

  return (
    <>
      <div className="dashboard-title-container">
        <div className="dashboard-title-text">Cell ({content.cellId})</div>
        <div className="dashboard-dropdown-container">
          <SortDropDown setOrderBy={setOrderBy} />
          <TimeDropDown />
        </div>
      </div>
      {/* Filter Bar */}
      <Form className="cell-filter-container">
        <div className="cell-checkbox-container">
          <Form.Check
            type="checkbox"
            label="Code"
            id="code-checkbox"
            checked={showInputs}
            onChange={event => {
              if (!event.target.checked && !showOutputs) {
                // Prevent unchecking both checkboxes
                event.preventDefault();
              } else {
                setShowInputs(event.target.checked);
              }
            }}
          />
          <Form.Check
            type="checkbox"
            label="Output"
            id="output-checkbox"
            checked={showOutputs}
            onChange={event => {
              if (!event.target.checked && !showInputs) {
                // Prevent unchecking both checkboxes
                event.preventDefault();
              } else {
                setShowOutputs(event.target.checked);
              }
            }}
          />
        </div>
        <div className="cell-radio-container">
          <ButtonGroup>
            {executionFilters.map((execFilter, idx) => (
              <ToggleButton
                key={idx}
                id={`filter-${idx}`}
                type="radio"
                variant="outline-primary"
                name="radio"
                value={execFilter.value}
                checked={radioValue === execFilter.value}
                onChange={e => setRadioValue(Number(e.currentTarget.value))}
              >
                {execFilter.name}
              </ToggleButton>
            ))}
          </ButtonGroup>
        </div>
      </Form>
      {isFetching ? (
        <Loader />
      ) : (
        <>
          {/* Cell Executions */}
          {apiData.map((value: { [key: string]: any }, index: number) => {
            return (
              <Row key={index}>
                {value.cell_type === 'MarkdownExecution' ? (
                  <Col md={12}>
                    <Card className="cell-card">
                      <Card.Body style={{ gap: '10px' }}>
                        <Row className="cell-card-wrapper">
                          <Col md={12} className="cell-user-title">
                            <Card.Text>User {index}</Card.Text>
                          </Col>
                          <Col md={12}>
                            <MarkdownComponent
                              markdownContent={value.cell_input}
                              markdownTranslator={props.markdownTranslator}
                            />
                          </Col>
                        </Row>
                      </Card.Body>
                    </Card>
                  </Col>
                ) : (
                  <>
                    {(radioValue === 1 ||
                      filterStatus[radioValue - 1] === value.status) && (
                      <Col md={12}>
                        <Card className="cell-card">
                          <Card.Body style={{ gap: '10px' }}>
                            <Row className="cell-card-wrapper">
                              <Col md={12} className="cell-user-title">
                                <Card.Text>User {index}</Card.Text>
                              </Col>
                              <Col md={12}>
                                {showInputs && (
                                  <CellInput
                                    cell_input={value.cell_input}
                                    language_mimetype={value.language_mimetype}
                                    className="cell-content-container"
                                  />
                                )}
                                {showInputs &&
                                  showOutputs &&
                                  value.cell_output_model.length > 0 && <br />}
                                {showOutputs &&
                                  value.cell_output_model.length > 0 && (
                                    <CellOutput
                                      cell_output_model={
                                        value.cell_output_model
                                      }
                                    />
                                  )}
                              </Col>
                            </Row>
                          </Card.Body>
                        </Card>
                      </Col>
                    )}
                  </>
                )}
              </Row>
            );
          })}
        </>
      )}
    </>
  );
};

export default Cell;
