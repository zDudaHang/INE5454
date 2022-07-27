import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, Legend, CartesianGrid } from 'recharts'
import { ServidorModel } from '../model'
import { Dictionary, forEach, groupBy, map, maxBy, reduce } from 'lodash'
import React from 'react'
import { randomHexColor } from './util'

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
    <div style={{ width: '100%', height: 500 }}>
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
          {cargos.map((cargo) => (
            <Bar dataKey={cargo} fill={randomHexColor()} />
          ))}
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
