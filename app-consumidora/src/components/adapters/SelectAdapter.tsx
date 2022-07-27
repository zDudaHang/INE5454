import { FormControl, Select } from 'bold-ui'
import React from 'react'

export const SelectAdapter = ({
  input: { onChange, value },
  label,
  name,
  items,
  itemToString,
  disabled,
  required,
  meta,
}: any) => {
  return (
    <FormControl error={meta.error} htmlFor='select-id' label={label} required={required}>
      <Select
        openOnFocus
        name={name}
        onChange={onChange}
        value={value}
        items={items}
        itemToString={itemToString}
        disabled={disabled}
        required={required}
      />
    </FormControl>
  )
}
