import React from 'react'
import { Button, Cell, Grid, VFlow } from 'bold-ui'
import { Field, Form, FormRenderProps } from 'react-final-form'

export interface GraficoFormModel {
  estados: string[]
  cargos: string[]
}

interface GraficoFormProps {
  estados: string[]
  cargos: string[]
  handleSubmit(values: GraficoFormModel): void
}

export function GraficoForm(props: GraficoFormProps) {
  const { cargos, estados, handleSubmit } = props

  const renderForm = (formProps: FormRenderProps<GraficoFormModel>) => {
    return (
      <Grid wrap justifyContent='center'>
        <Cell size={6}>
          <VFlow>
            <label>Cargos</label>
            <Field component='select' type='select' name='cargos' multiple>
              {cargos.map((cargo) => (
                <option key={cargo} value={cargo}>
                  {cargo}
                </option>
              ))}
            </Field>
          </VFlow>
        </Cell>
        <Cell size={6}>
          <VFlow>
            <label>Estados</label>
            <Field component='select' type='select' name='estados' multiple>
              {estados.map((estado) => (
                <option key={estado} value={estado}>
                  {estado}
                </option>
              ))}
            </Field>
          </VFlow>
        </Cell>
        <Cell size={12}>
          <Button type='submit' kind='primary' onClick={formProps.handleSubmit}>
            Gerar gráfico
          </Button>
        </Cell>
      </Grid>
    )
  }

  return <Form<GraficoFormModel> render={renderForm} onSubmit={handleSubmit} />
}
