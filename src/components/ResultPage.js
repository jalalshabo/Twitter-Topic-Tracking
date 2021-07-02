import React from 'react'
import {Bar, Scatter} from 'react-chartjs-2';
import './ResultPage.css';  
function ResultPage() {
    const rand = () => Math.round(Math.random() * 20 - 10); 

    const bar_state = {
      labels: ['Word1', 'Word2', 'Word3',
                'Word4', 'Word5'],
      datasets: [
        {
          label: 'User1',
          backgroundColor: ['rgba(75,192,192,1)'],
          borderColor: 'rgba(0,0,0,1)',
          borderWidth: 2,
          data: [65, 59, 80, 81, 56]
        },
        {
          label: 'User2',
          backgroundColor: ['#FD668C'],
          borderColor: 'rgba(0,0,0,1)',
          borderWidth: 2,
          data: [31, 90, 60, 101, 46]
        }
      ]
    }

    const scatter_state = { 
      datasets: [
        {
          label: 'Test scatter graph',
          data: [
            { x: rand(), y: rand() },
            { x: rand(), y: rand() },
            { x: rand(), y: rand() },
            { x: rand(), y: rand() },
            { x: rand(), y: rand() },
            { x: rand(), y: rand() },
            { x: rand(), y: rand() },
            { x: rand(), y: rand() },
            { x: rand(), y: rand() },
            { x: rand(), y: rand() },
            { x: rand(), y: rand() },
            { x: rand(), y: rand() },
            { x: rand(), y: rand() },
            { x: rand(), y: rand() },
          ],
          backgroundColor: '#000',
        }
      ]         
    }
  
    const scatter_options = {
    scales: {
        yAxes: [
          {
            ticks: {
              beginAtZero: true,
            },
          },
        ],
      },
    };
  
    return (
      <>
       
        <div className="result-wrapper">

            <div className="result-graph">
              <Scatter data= {scatter_state} options={scatter_options} />
            </div>

            <div className="result-graph">
              <Bar
              data={bar_state}
              options={{
                  title:{
                  display:true,
                  text:'Topic Tracking found within Users',
                  fontSize:50,
                  },
                  legend:{
                  display:true,
                  position:'right'
                  }
              }}
              />
            </div>

        </div>
      </>
    );

 

}

export default ResultPage
