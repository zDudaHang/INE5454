import { FileUploader, VFlow, Heading } from 'bold-ui'
import React, { useState } from 'react'
import './App.css'
import { GraficosView } from './components/GraficosView'
import { ServidorJSONModel, ServidorModel } from './model'

function App() {
  const [servidores, setServidores] = useState<ServidorModel[]>([])
  const [cargos, setCargos] = useState<Set<string>>(new Set())
  const [estados, setEstados] = useState<Set<string>>(new Set())

  function converJSONModelToServidorModel(servidor: ServidorJSONModel): ServidorModel {
    const { NOME, CARGO, ORGAO, PORTAL, REMUNERACAO } = servidor

    if (!cargos.has(CARGO)) setCargos(new Set(cargos.add(CARGO)))
    if (!estados.has(PORTAL)) setEstados(new Set(estados.add(PORTAL)))

    return {
      nome: NOME,
      cargo: CARGO,
      orgao: ORGAO,
      portal: PORTAL,
      remuneracao: parseFloat(REMUNERACAO),
    }
  }

  const handleDropAccepted = (files: File[]) => {
    files.forEach((file) => {
      file.text().then((text) => {
        const servidoresJSON = JSON.parse(text) as ServidorJSONModel[]
        const novosServidores = servidoresJSON.map(converJSONModelToServidorModel)
        setServidores([...servidores, ...novosServidores])
      })
    })
  }

  return (
    <VFlow>
      <FileUploader onDropAccepted={handleDropAccepted} text='Importe os servidores aqui' />
      {servidores.length !== 0 ? (
        <GraficosView servidores={servidores} estados={estados} cargos={cargos} />
      ) : (
        <Heading level={2}>Primeiro, importe os servidores</Heading>
      )}
    </VFlow>
  )
}

export default App
