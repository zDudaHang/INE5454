import { css } from '@emotion/core'
import { FileUploader, HFlow } from 'bold-ui'
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

  return servidores.length !== 0 ? (
    <GraficosView servidores={servidores} estados={Array.from(estados)} cargos={Array.from(cargos)} />
  ) : (
    <HFlow style={styles.container} justifyContent='center'>
      <FileUploader onDropAccepted={handleDropAccepted} text='Importe os servidores aqui' />
    </HFlow>
  )
}

const styles = {
  heading: css`
    text-align: center;
  `,
  container: css`
    margin-top: 1rem;
  `,
}

export default App
