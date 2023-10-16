import React, { useEffect, useState, useRef } from 'react';
import { NotebookPanel } from '@jupyterlab/notebook';
import NoNotebookPlaceholder from '../toc-dashboard/NoNotebookPlaceholder';
import { useSelector } from 'react-redux';
import PageRouter from './PageRouter';
import { RootState } from '../redux/store';
import SidebarPlaceholder from './SidebarPlaceholder';
import { BACKEND_API_URL, Selectors } from '../utils/constants';
import { hashCellList } from '../utils/utils';
import Loader from './components/placeholder/Loader';
import { IMarkdownTranslator } from '../plugins/sideDashboard';

interface IDashboardProps {
  panel: NotebookPanel | null;
  markdownTranslator: IMarkdownTranslator;
}

const DashboardComponent = (props: IDashboardProps): JSX.Element => {
  const notebookCells = useSelector(
    (state: RootState) => state.commondashboard.notebookCells
  );

  const [isChecking, setIsChecking] = useState<boolean>(true);
  const [invalidity, setInvalidity] = useState<null | string>(null);
  const [hasValidNotebookId, setHasValidNotebookId] = useState<
    string | null | undefined
  >(null);

  const currentRequestId = useRef<string>('12345678');
  useEffect(() => {
    const fetchData = async () => {
      let validNotebookId = null;
      let invalidityReason: string | null = 'No Notebook';
      if (props.panel && props.panel.model) {
        setIsChecking(true);
        // only fetch when the panel has finished building
        if (props.panel.context.isReady) {
          invalidityReason = 'Fetching Error';
          const notebookId = props.panel.model.getMetadata(
            Selectors.notebookId
          );

          try {
            if (notebookId) {
              const newRequestId = crypto.randomUUID();
              currentRequestId.current = newRequestId;

              const response = await fetch(
                `${BACKEND_API_URL}/dashboard/check/${notebookId}?hashedList=${hashCellList(
                  notebookCells?.map(c => c.id)
                )}`
              );

              if (newRequestId === currentRequestId.current) {
                if (response.ok) {
                  const data = await response.json();
                  if (data.status === 'not_found') {
                    // no entry found in the Notebook table for the notebook id
                    invalidityReason = 'Notebook not Registered';
                  } else if (data.status === 'hash_mismatch') {
                    // hash mismatch between the URL parameter and the notebook table entry
                    invalidityReason = 'Mismatch with the Registered Notebook';
                  } else if (data.status === 'success') {
                    invalidityReason = null;
                    validNotebookId = notebookId;
                  }
                }
              }
            } else {
              invalidityReason = 'Untagged Notebook';
            }
          } catch (error) {
            console.log('(Check your connexion) ' + error);
          }
        }
      }
      setIsChecking(false);
      setInvalidity(invalidityReason);
      setHasValidNotebookId(validNotebookId);
    };

    // call the async fetch method
    fetchData();
  }, [props.panel, notebookCells]);

  return (
    <>
      {props.panel ? (
        <>
          {isChecking ? (
            <Loader />
          ) : (
            <>
              {invalidity ? (
                <SidebarPlaceholder title={invalidity} />
              ) : (
                <PageRouter
                  notebookId={hasValidNotebookId as string}
                  notebookName={props.panel.sessionContext.name}
                  markdownTranslator={props.markdownTranslator}
                />
              )}
            </>
          )}
        </>
      ) : (
        <NoNotebookPlaceholder title={'Side Panel Dashboard'} />
      )}
    </>
  );
};

export default DashboardComponent;
