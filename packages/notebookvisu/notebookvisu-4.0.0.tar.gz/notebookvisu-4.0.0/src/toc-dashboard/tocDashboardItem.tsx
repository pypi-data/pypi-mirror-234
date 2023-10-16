import React from 'react';
import { INotebookHeading } from '../utils/headings';
import { ItemRenderer } from '../utils/interfaces';
import TocReactComponent from './TocReactComponent';
import { CommandRegistry } from '@lumino/commands';

interface ITocDashboardItemProps {
  heading: INotebookHeading;

  headings: INotebookHeading[];

  itemRenderer: ItemRenderer;

  addReactComponent: boolean;

  isFirstCellOccurrence: boolean;

  tocDashboardData:
    | [number | null | undefined, number | null | undefined]
    | null;

  commands: CommandRegistry;
}

export class TocDashboardItem extends React.Component<ITocDashboardItemProps> {
  render() {
    const {
      heading,
      headings,
      addReactComponent,
      isFirstCellOccurrence,
      tocDashboardData,
      commands
    } = this.props;

    // create an onClick handler for the TOC item
    // that scrolls the anchor into view.
    const onClick = (event: React.SyntheticEvent<HTMLSpanElement>) => {
      event.preventDefault();
      event.stopPropagation();
      heading.onClick();
    };

    const content = this.props.itemRenderer(heading, headings);
    if (!content) {
      return null;
    }
    return (
      <li className="dashboard-tocItem" onClick={onClick}>
        {content}
        {addReactComponent && (
          <TocReactComponent
            cellId={heading.cellRef.model.id}
            data={isFirstCellOccurrence ? tocDashboardData : null}
            commands={commands}
          />
        )}
      </li>
    );
  }
}

export default TocDashboardItem;
