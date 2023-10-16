import React from 'react';

const SidebarPlaceholder = ({ title }: { title: string }): JSX.Element => {
  return (
    <div className="dashboard-TableOfContents">
      <div className="dashboard-stack-panel-header">Side Panel Dashboard</div>
      <div className="dashboard-TableOfContents-placeholder">
        <div className="dashboard-TableOfContents-placeholderContent">
          <h3>{title}</h3>
          <p>No data for the opened notebook.</p>
        </div>
      </div>
    </div>
  );
};

export default SidebarPlaceholder;
