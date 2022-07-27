import { VFlow } from 'bold-ui'
import React, { useState } from 'react'
import { ServidorModel } from '../model'
import { GraficoForm, GraficoFormModel } from './GraficoForm'
import { GraficoSalarioPorCargo } from './GraficoSalarioPorCargo'

interface GraficosViewProps {
  servidores: ServidorModel[]
  estados: string[]
  cargos: string[]
}

export function GraficosView(props: GraficosViewProps) {
  const { servidores, cargos, estados } = props

  const [servidoresFiltrados, setServidoresFiltrados] = useState<ServidorModel[]>([])
  const [cargosSelecionados, setCargosSelecionados] = useState<string[]>([])

  const handleSubmit = (values: GraficoFormModel) => {
    const { cargos: cargosSelecionados, estados: estadosSelecionados } = values
    const servidoresSelecionados = servidores.filter(
      (servidor) => cargosSelecionados.includes(servidor.cargo) && estadosSelecionados.includes(servidor.portal)
    )
    setServidoresFiltrados(servidoresSelecionados)
    setCargosSelecionados([...cargosSelecionados])
  }

  return (
    <VFlow>
      <GraficoForm handleSubmit={handleSubmit} estados={estados} cargos={cargos} />
      {servidoresFiltrados.length > 0 && cargosSelecionados.length > 0 && (
        <GraficoSalarioPorCargo servidores={servidoresFiltrados} cargos={cargosSelecionados} />
      )}
    </VFlow>
  )
}
