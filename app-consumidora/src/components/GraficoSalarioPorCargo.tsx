import { ResponsiveContainer, BarChart, Bar } from 'recharts'
import { ServidorModel } from '../model'
import React from 'react'

interface GraficoSalarioPorCargoProps {
  servidores: ServidorModel[]
}

export function GraficoSalarioPorCargo(props: GraficoSalarioPorCargoProps) {
  const { servidores } = props

  return (
    <div style={{ width: '100%', height: 300 }}>
      <ResponsiveContainer>
        <BarChart width={150} height={40} data={[]}>
          <Bar dataKey='remuneracao' fill='#8884d8' />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
