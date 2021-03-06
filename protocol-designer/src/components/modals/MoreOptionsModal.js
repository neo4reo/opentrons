// @flow
import * as React from 'react'
import {
  FlatButton,
  PrimaryButton,
  FormGroup,
  InputField,
  Modal
} from '@opentrons/components'

import type {FormModalFields} from '../../steplist/types'
import {formConnectorFactory} from '../../utils'
import styles from './MoreOptionsModal.css'
import modalStyles from './modal.css'

type Props = {
  onDelete: (event: SyntheticEvent<>) => void,
  onCancel: (event: SyntheticEvent<>) => void,
  onSave: (event: SyntheticEvent<>) => void,
  handleChange: (accessor: string) => (event: SyntheticEvent<HTMLInputElement> | SyntheticEvent<HTMLSelectElement>) => void,
  formData: FormModalFields,
  hideModal: boolean
}

export default function (props: Props) {
  const formConnector = formConnectorFactory(props.handleChange, props.formData)
  return (
    !props.hideModal && <Modal onCloseClick={props.onCancel} className={modalStyles.modal}>
      <div className={modalStyles.modal_contents}>
        <FormGroup label='Step Name' className={styles.column_1_2}>
          <InputField {...formConnector('step-name')} />
        </FormGroup>
        <FormGroup label='Step Notes' className={styles.column_1_2}>
          {/* TODO: need textarea input in component library for big text boxes. */}
          <textarea className={styles.big_text_box} {...formConnector('step-details')} />
        </FormGroup>
        <div className={styles.button_row}>
          <PrimaryButton onClick={props.onDelete}>DELETE STEP</PrimaryButton> {/* TODO! */}
          <FlatButton onClick={props.onCancel}>CANCEL</FlatButton>
          <FlatButton onClick={props.onSave}>SAVE</FlatButton>
        </div>
      </div>
    </Modal>
  )
}
