import React from 'react'
import {Bar} from 'react-chartjs-2';
import './ResultPage.css';
function ResultPage() {
   
    const graph_state = {
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
    
    return (
        <>
            <h1> Topic Tracking Results: </h1>
            <div className="result-graph">
            <Bar
            data={graph_state}
            options={{
                title:{
                display:true,
                text:'Average Rainfall per month',
                fontSize:50,
                },
                legend:{
                display:true,
                position:'right'
                }
            }}
            />
        </div>
      </>
    );

 

}

export default ResultPage
