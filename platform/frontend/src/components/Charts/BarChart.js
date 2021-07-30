import React, {PureComponent} from 'react';
import {Bar, BarChart, CartesianGrid, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis} from 'recharts';

const data = [
    {
        name: '0 - 18',
        homme: 10,
        femme: 5,
    },
    {
        name: '18 - 25',
        homme: 21,
        femme: 22,
    },
    {
        name: '25 - 35',
        homme: 23,
        femme: 40,
    },
    {
        name: '35 - 45',
        homme: 50,
        femme: 22,
    },
    {
        name: '45 - 55',
        homme: 42,
        femme: 56,
    },
    {
        name: '55 - 65',
        homme: 10,
        femme: 25,
    },
    {
        name: '65 et plus',
        homme: 70,
        femme: 55,
    },
];

export default class Example extends PureComponent {
    static demoUrl = 'https://codesandbox.io/s/mixed-bar-chart-q4hgc';

    render() {
        return (
            <ResponsiveContainer width="100%" height="100%">
                <BarChart
                    width={500}
                    height={300}
                    data={data}
                    margin={{
                        top: 20,
                        right: 30,
                        left: 20,
                        bottom: 5,
                    }}
                >
                    <CartesianGrid strokeDasharray="3 3"/>
                    <XAxis dataKey="name"/>
                    <YAxis/>
                    <Tooltip/>
                    <Legend/>
                    <Bar dataKey="homme" stackId="a" fill="#8884d8"/>
                    <Bar dataKey="femme" stackId="a" fill="#82ca9d"/>
                </BarChart>
            </ResponsiveContainer>
        );
    }
}
