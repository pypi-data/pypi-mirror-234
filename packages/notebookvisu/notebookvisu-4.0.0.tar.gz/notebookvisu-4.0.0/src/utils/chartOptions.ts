export const locationOptions = {
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false,
      labels: {
        color: '#969696'
      }
    }
  },
  scales: {
    x: {
      title: {
        display: true,
        text: 'Cell (markdown & code)',
        color: '#969696'
      },
      ticks: {
        color: '#969696'
      }
    },
    y: {
      ticks: {
        beginAtZero: true,
        precision: 0,
        color: '#969696'
      },
      title: {
        display: true,
        text: 'Number of users',
        color: '#969696'
      }
    }
  }
};

export const codeExecOptions = {
  maintainAspectRatio: false,
  plugins: {
    legend: {
      labels: {
        color: '#969696'
      }
    }
  },
  scales: {
    x: {
      title: {
        display: true,
        text: 'Code cell',
        color: '#969696'
      },
      ticks: {
        color: '#969696'
      }
    },
    y: {
      // max: 100,
      ticks: {
        beginAtZero: true,
        precision: 0,
        color: '#969696'
      },
      title: {
        display: true,
        text: 'Cumulated total across all users',
        color: '#969696'
      }
    }
  }
};

export const timeSpentOptions = {
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: true,
      labels: {
        usePointStyle: true,
        color: '#969696'
      }
    },
    tooltip: {
      callbacks: {
        title: function (tooltipItem: any) {
          return `Cell ${tooltipItem[0].raw.x}`;
        },
        label: function (tooltipItem: any) {
          return `t: ${tooltipItem.raw.y}`;
        }
      }
    }
  },
  scales: {
    x: {
      type: 'category' as const,
      ticks: {
        color: '#969696'
      },
      title: {
        display: true,
        text: 'Cell (markdown & code)',
        color: '#969696'
      }
    },
    y: {
      ticks: {
        beginAtZero: true,
        precision: 0,
        color: '#969696'
      },
      title: {
        display: true,
        text: 'Time spent on a cell [s]',
        color: '#969696'
      }
    }
  }
};
