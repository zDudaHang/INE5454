import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, Legend, CartesianGrid } from 'recharts'
import { ServidorModel } from '../model'
import { forEach, groupBy, maxBy } from 'lodash'
import { randomHexColor } from './util'
import React from 'react'

interface GraficoSalarioPorCargoProps {
  servidores: ServidorModel[]
  cargos: string[]
}

export function GraficoSalarioPorCargo(props: GraficoSalarioPorCargoProps) {
  const { servidores, cargos } = props

  const servidoresTeste: any[] = []

  const servidoresAgrupadosPorPortal = groupBy(servidores, 'portal')
  forEach(servidoresAgrupadosPorPortal, (servidoresPorPortal, portal) => {
    const servidoresAgrupadosPorCargo = groupBy(servidoresPorPortal, 'cargo')
    const servidor = { portal }
    forEach(servidoresAgrupadosPorCargo, (servidoresPorCargo, cargo) => {
      const remuneracaoMaxima = maxBy(servidoresPorCargo, 'remuneracao').remuneracao
      Object.assign(servidor, { [cargo]: remuneracaoMaxima })
    })
    servidoresTeste.push(servidor)
  })

  return (
    <div style={{ justifyContent: 'center', alignContent: 'center', marginTop: '2rem', width: '100%', height: 600 }}>
      <ResponsiveContainer>
        <BarChart
          width={150}
          height={40}
          data={servidoresTeste}
          margin={{
            top: 5,
            right: 30,
            left: 20,
            bottom: 5,
          }}
        >
          <CartesianGrid strokeDasharray='3 3' />
          <XAxis dataKey='portal' />
          <YAxis />
          <Tooltip />
          <Legend />
          {cargos.map((cargo, index) => (
            <Bar key={index} dataKey={cargo} fill={randomHexColor()} />
          ))}
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
