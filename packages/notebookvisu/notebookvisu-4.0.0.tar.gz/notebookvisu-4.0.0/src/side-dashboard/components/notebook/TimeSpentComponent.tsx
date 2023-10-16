import React, { useEffect, useState } from 'react';
import { ChartData } from 'chart.js';
import { BACKEND_API_URL } from '../../../utils/constants';
import { NotebookCell } from '../../../redux/types';
import ChartContainer from './ChartContainer';
import { Scatter } from 'react-chartjs-2';
import { timeSpentOptions } from '../../../utils/chartOptions';
import { IChartProps } from '../../pages/Notebook';

const TimeSpentComponent = (props: IChartProps) => {
  const [timeSpentData, setTimeSpentData] = useState<ChartData<'scatter'>>({
    labels: [],
    datasets: []
  });

  // fetching access time data
  useEffect(() => {
    fetch(
      `${BACKEND_API_URL}/dashboard/${props.notebookId}/user_cell_time?timeWindow=${props.timeWindow}`
    )
      .then(response => response.json())
      .then(data => {
        const chartData: ChartData<'scatter'> = {
          labels: props.notebookCells
            ? Array.from(
                { length: props.notebookCells.length },
                (_, index) => index + 1
              )
            : [],
          datasets: [
            {
              label: 'time spent on a cell by a user',
              data:
                props.notebookCells?.flatMap(
                  (cell: NotebookCell, index: number) => {
                    const foundData = data.find(
                      (item: any) => item.cell === cell.id
                    );
                    if (foundData) {
                      return foundData.durations.map((d: number) => ({
                        x: index + 1,
                        y: d
                      }));
                    }
                    return [];
                  }
                ) || [],
              backgroundColor: 'rgba(54, 162, 235, 0.2)',
              borderColor: 'rgba(54, 162, 235, 1)',
              borderWidth: 1,
              pointRadius: 1
            }
          ]
        };
        setTimeSpentData(chartData);
      });
  }, [props.timeWindow, props.refreshRequired]);

  return (
    <ChartContainer
      PassedComponent={
        <Scatter data={timeSpentData} options={timeSpentOptions} />
      }
      title="Amount of time spent on each cell"
    />
  );
};

export default TimeSpentComponent;
