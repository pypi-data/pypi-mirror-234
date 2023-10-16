import React, { useEffect, useRef } from 'react';
import { useSelector } from 'react-redux';
import { RootState } from '../redux/store';
import { NotebookPanel } from '@jupyterlab/notebook';
import { INotebookHeading } from '../utils/headings';
import { TocDashboardItem } from './tocDashboardItem';
import { ItemRenderer } from '../utils/interfaces';
import { BACKEND_API_URL, Selectors } from '../utils/constants';
import { hashCellList } from '../utils/utils';
import { LocationData } from '../redux/types';
import { CommandRegistry } from '@lumino/commands';
import { AppDispatch, store } from '../redux/store';
import { setFetchedLocationData } from '../redux/reducers/ToCDashboardReducer';
const dispatch = store.dispatch as AppDispatch;

interface ITOCTreeProps {
  headings: INotebookHeading[];
  itemRenderer: ItemRenderer;
  notebookPanel: NotebookPanel;
  commands: CommandRegistry;
  notebookCells: string[] | null | undefined;
}

const TocDashboardTree: React.FC<ITOCTreeProps> = props => {
  // locationData is reset to null when the cell list changes in TocDashboardPanel
  const locationData = useSelector(
    (state: RootState) => state.tocdashboard.locationData
  );
  const shouldDisplayDashboardRedux = useSelector(
    (state: RootState) => state.tocdashboard.displayDashboard
  );
  const refreshRequired = useSelector(
    (state: RootState) => state.commondashboard.refreshBoolean
  );
  const timeWindow = useSelector(
    (state: RootState) => state.commondashboard.timeWindow
  );

  // only fetch again when the list of cells actually changed or when a refresh is requested
  useEffect(() => {
    fetchToCData();
  }, [props.notebookCells, refreshRequired, timeWindow, props.notebookPanel]);

  // id to make sure only the last request resolves
  const currentRequestId = useRef<string>('12345678');
  const fetchToCData = async (): Promise<void> => {
    const notebookId = props.notebookPanel.model?.getMetadata(
      Selectors.notebookId
    );
    // only fetch if there is a notebook id, and there are cells
    if (!notebookId || !props.notebookCells) {
      return;
    }
    try {
      const newRequestId = crypto.randomUUID();
      currentRequestId.current = newRequestId;

      const response = await fetch(
        `${BACKEND_API_URL}/dashboard/toc/${notebookId}?hashedList=${hashCellList(
          props.notebookCells
        )}&timeWindow=${timeWindow}`
      );

      // check that it's the response from the current request and not a subsequent
      if (newRequestId === currentRequestId.current) {
        if (response.ok) {
          const data = await response.json();
          // process the response data and handle the different scenarios
          if (data.status === 'not_found') {
            // no entry found in the Notebook table for the notebook id
            console.log('Notebook not registered');
          } else if (data.status === 'hash_mismatch') {
            // hash mismatch between the URL parameter and the notebook table entry
            console.log('Cell list mismatch with the registered notebook');
          } else if (data.status === 'success') {
            dispatch(setFetchedLocationData(data.data));
            return;
          }
        } else {
          console.log('Error:', response.status);
        }
      }
    } catch (error) {
      console.log('Toc Fetch Error:', error);
    }
    // if it didn't fetch, set the fetched data to null
    dispatch(setFetchedLocationData(null));
  };

  const aggregateCollapsedData = (
    value: LocationData
  ): { [key: string]: number } => {
    const uncollapsedIds: string[] = props.headings.map(
      heading => heading.cellRef.model.id
    );
    const uniqueUncollapsedIds: string[] = [...new Set(uncollapsedIds)];

    const dict: { [key: string]: number } = {};
    const cells = props.notebookCells;
    if (cells && value) {
      const mapping: number[] = uniqueUncollapsedIds.map(id =>
        cells.indexOf(id)
      );

      dict['total_count'] = value.total_count;

      // adapt the boundaries
      mapping[0] = 0;
      mapping.push(cells.length - 1);

      for (let i = 0; i < uniqueUncollapsedIds.length; i++) {
        const start = mapping[i];
        const end = mapping[i + 1];
        let total = 0;
        if (start === -1) {
          // not found
          total = 0;
        } else {
          for (let j = start; j < end; j++) {
            total += value.location_count[cells[j]] || 0;
          }
        }
        dict[uniqueUncollapsedIds[i]] = total;
      }
    }

    return dict;
  };

  // on every re-render, aggregate locationData from collapsed headings
  const aggregatedData = aggregateCollapsedData(locationData);

  const renderedCells = new Set<string>();
  return (
    <ul className="dashboard-TableOfContents-content">
      {props.headings.map((el, index) => {
        const cellId = el.cellRef.model.id;
        const isFirstCellOccurrence = !renderedCells.has(cellId);

        if (isFirstCellOccurrence) {
          renderedCells.add(cellId);
        }
        return (
          <TocDashboardItem
            heading={el}
            headings={props.headings}
            itemRenderer={props.itemRenderer}
            // only display the dashboard component when not disabled with redux, when it's the first cell occurrence and when there is data
            addReactComponent={shouldDisplayDashboardRedux && !!locationData}
            isFirstCellOccurrence={isFirstCellOccurrence}
            tocDashboardData={[
              aggregatedData[cellId],
              aggregatedData['total_count']
            ]}
            commands={props.commands}
            key={`${el.text}-${el.level}-${index++}`}
          />
        );
      })}
    </ul>
  );
};

export default TocDashboardTree;
