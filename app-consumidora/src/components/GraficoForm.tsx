/** @jsx jsx */
import { jsx, css } from '@emotion/core'
import { Button, Cell, Grid, HFlow, isEqual } from 'bold-ui'
import { Field, Form, FormRenderProps } from 'react-final-form'
import { SelectField } from './SelectField'

export interface GraficoFormModel {
  estados: string[]
  cargos: string[]
}

interface GraficoFormProps {
  estados: string[]
  cargos: string[]
  handleSubmit(values: GraficoFormModel): void
}

const itemToString = (item: string) => item

export function GraficoForm(props: GraficoFormProps) {
  const { cargos, estados, handleSubmit } = props

  const renderForm = (formProps: FormRenderProps<GraficoFormModel>) => {
    return (
      <Grid wrap style={styles.container} justifyContent='center'>
        <Cell size={6}>
          <Field
            name='cargos'
            render={(props) => (
              <SelectField
                {...props}
                label='Cargos'
                placeholder='Selecione os cargos que queira filtrar'
                items={cargos}
                itemToString={itemToString}
                itemIsEqual={isEqual}
                multiple
                clearable
                required
              />
            )}
          />
        </Cell>
        <Cell size={6}>
          <Field
            name='estados'
            render={(props) => (
              <SelectField
                {...props}
                name='estados'
                label='Estados'
                placeholder='Selecione os estados que queira filtrar'
                items={estados}
                itemToString={itemToString}
                itemIsEqual={isEqual}
                multiple
                clearable
                required
              />
            )}
          />
        </Cell>
        <Cell size={6} style={styles.buttonsContainer}>
          <HFlow justifyContent='flex-end'>
            <Button kind='primary' size='medium' onClick={formProps.handleSubmit}>
              Gerar gráfico
            </Button>
          </HFlow>
        </Cell>
      </Grid>
    )
  }

  return <Form<GraficoFormModel> render={renderForm} onSubmit={handleSubmit} />
}

const styles = {
  container: css`
    margin-top: 2rem;
  `,
  buttonsContainer: css`
    padding-left: 2rem;
    padding-right: 0;
  `,
}
