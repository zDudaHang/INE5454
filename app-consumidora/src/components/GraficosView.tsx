import { VFlow } from 'bold-ui'
import React from 'react'
import { ServidorModel } from '../model'
import { GraficoForm } from './GraficoForm'
import { GraficoSalarioPorCargo } from './GraficoSalarioPorCargo'

interface GraficosViewProps {
  servidores: ServidorModel[]
  estados: Set<string>
  cargos: Set<string>
}

export function GraficosView(props: GraficosViewProps) {
  const { servidores, ...formProps } = props

  const handleCargosChange = (cargos: string[]) => {}

  const handleEstadosChange = (estados: string[]) => {}

  // const servidoresFiltrados = useMemo(
  //   () =>
  //     servidores.filter(
  //       (servidor) => cargosSelecionados.includes(servidor.cargo) && estadosSelecionados.includes(servidor.portal)
  //     ),
  //   [cargosSelecionados, estadosSelecionados, servidores]
  // )

  return (
    <VFlow>
      <GraficoForm handleSubmit={console.log} {...formProps} />
      <GraficoSalarioPorCargo servidores={servidores} />
    </VFlow>
  )
}
