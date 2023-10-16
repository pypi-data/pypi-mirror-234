import React, { useEffect, useState } from 'react';
import { ChartData } from 'chart.js';
import { BACKEND_API_URL } from '../../../utils/constants';
import ChartContainer from './ChartContainer';
import { Bar } from 'react-chartjs-2';
import { codeExecOptions } from '../../../utils/chartOptions';
import { IChartProps } from '../../pages/Notebook';

const CodeExecComponent = (props: IChartProps) => {
  const [codeExecData, setCodeExecData] = useState<ChartData<'bar'>>({
    labels: [],
    datasets: []
  });

  // fetching execution data
  useEffect(() => {
    fetch(
      `${BACKEND_API_URL}/dashboard/${props.notebookId}/user_code_execution?timeWindow=${props.timeWindow}`
    )
      .then(response => response.json())
      .then(data => {
        // filter elements of notebookCells that are of type 'code'
        const codeCells =
          props.notebookCells?.filter(cell => cell.cellType === 'code') || [];

        const chartData: ChartData<'bar'> = {
          labels: Array.from(
            { length: codeCells.length },
            (_, index) => index + 1
          ),
          datasets: [
            {
              label: 'clicks',
              data: Array(codeCells.length).fill(null),
              backgroundColor: 'rgba(54, 162, 235, 0.2)',
              borderColor: 'rgba(54, 162, 235, 1)',
              borderWidth: 1
            },
            {
              label: 'executions',
              data: Array(codeCells.length).fill(null),
              backgroundColor: 'rgba(255, 99, 132, 0.2)',
              borderColor: 'rgba(255,99,132,1)',
              borderWidth: 1
            },
            {
              label: 'executions without errors',
              data: Array(codeCells.length).fill(null),
              backgroundColor: 'rgba(75, 192, 192, 0.2)',
              borderColor: 'rgba(75, 192, 192, 1)',
              borderWidth: 1
            }
          ]
        };

        // iterate through codeCells and find corresponding datasets from data
        codeCells.forEach((codeCell, index) => {
          const matchingData = data.find(
            (item: any) => item.cell === codeCell.id
          );
          if (matchingData) {
            chartData.datasets[0].data[index] = parseFloat(
              matchingData.cell_click_pct
            );
            chartData.datasets[1].data[index] = parseFloat(
              matchingData.code_exec_pct
            );
            chartData.datasets[2].data[index] = parseFloat(
              matchingData.code_exec_ok_pct
            );
          }
        });
        setCodeExecData(chartData);
      });
  }, [props.timeWindow, props.refreshRequired]);

  return (
    <ChartContainer
      PassedComponent={<Bar data={codeExecData} options={codeExecOptions} />}
      title="Code cell execution across users"
    />
  );
};

export default CodeExecComponent;
