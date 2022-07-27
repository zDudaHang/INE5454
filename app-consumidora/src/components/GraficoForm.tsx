import React from 'react'
import { css } from '@emotion/core'
import { Button, Cell, Grid, Heading, HFlow, isEqual, VFlow } from 'bold-ui'
import { Field, Form, FormRenderProps } from 'react-final-form'
import { SelectAdapter } from './adapters/SelectAdapter'

interface GraficoFormProps {
  estados: Set<string>
  cargos: Set<string>
  handleSubmit(values: GraficoFormModel): void
}

interface GraficoFormModel {
  estados: string[]
  cargos: string[]
}

const itemToString = (item: string) => item

export function GraficoForm(props: GraficoFormProps) {
  const { cargos, estados, handleSubmit } = props

  const renderForm = (formProps: FormRenderProps<GraficoFormModel>) => {
    return (
      <Grid wrap justifyContent='center'>
        <Cell size={6}>
          <Field
            component={SelectAdapter}
            name='cargos'
            label='Cargos'
            placeholder='Selecione os cargos'
            items={Array.from(cargos)}
            itemToString={itemToString}
            itemIsEqual={isEqual}
            clearable
          />
        </Cell>
        <Cell size={6}>
          <Field
            component={SelectAdapter}
            name='estados'
            label='Estados'
            placeholder='Selecione os estados'
            items={Array.from(estados)}
            itemToString={itemToString}
            itemIsEqual={isEqual}
            clearable
          />
        </Cell>
        <Cell size={12}>
          <Button type='submit' kind='primary' onClick={formProps.handleSubmit}>
            Gerar gráfico
          </Button>
        </Cell>
      </Grid>
    )
  }

  return (
    <VFlow>
      <Heading level={2}>Gráfico</Heading>
      <Form<GraficoFormModel> render={renderForm} onSubmit={handleSubmit} />
    </VFlow>
  )
}
