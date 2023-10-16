import React from 'react';

const NoNotebookPlaceholder = ({ title }: { title: string }): JSX.Element => {
  return (
    <div className="dashboard-TableOfContents">
      <div className="dashboard-stack-panel-header">{title}</div>
      <div className="dashboard-TableOfContents-placeholder">
        <div className="dashboard-TableOfContents-placeholderContent">
          <h3>No Notebook</h3>
          <p>Open a notebook to start viewing its content.</p>
        </div>
      </div>
    </div>
  );
};

export default NoNotebookPlaceholder;
