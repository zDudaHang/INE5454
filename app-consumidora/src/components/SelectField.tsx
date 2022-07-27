import { Select } from 'bold-ui'
import React from 'react'
import { FieldRenderProps } from 'react-final-form'

interface SelectFieldProps<FieldValue> extends FieldRenderProps<FieldValue> {
  label: string
  placeholder: string
  multiple?: boolean
  required?: boolean
  items: FieldValue[]

  itemToString(item: FieldValue): string
  itemIsEqual(a: FieldValue, b: FieldValue): boolean
}

export function SelectField<FieldValue>(props: SelectFieldProps<FieldValue>) {
  const {
    input: { onChange, value, name },
    ...rest
  } = props
  return <Select name={name} {...rest} onChange={onChange} value={value} />
}
