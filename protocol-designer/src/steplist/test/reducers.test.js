// @flow
import {_allReducers} from '../reducers.js'

const {
  steps,
  collapsedSteps,
  orderedSteps,
  selectedStep,
  stepCreationButtonExpanded
} = _allReducers

describe('steps reducer', () => {
  test('initial add step', () => {
    const state = {}
    const action = {
      type: 'ADD_STEP',
      payload: {id: 123, stepType: 'transfer'}
    }

    expect(steps(state, action)).toEqual({
      '123': {
        id: 123,
        stepType: 'transfer',
        title: 'transfer' // title gets added
      }
    })
  })

  test('second add step', () => {
    const state = {
      '333': {
        id: 333,
        stepType: 'mix',
        title: 'mix'
      }
    }
    const action = {
      type: 'ADD_STEP',
      payload: {id: 123, stepType: 'transfer'}
    }

    expect(steps(state, action)).toEqual({
      '333': {
        id: 333,
        stepType: 'mix',
        title: 'mix'
      },
      '123': {
        id: 123,
        stepType: 'transfer',
        title: 'transfer'
      }
    })
  })
})

describe('collapsedSteps reducer', () => {
  test('add step', () => {
    const state = {}
    const action = {
      type: 'ADD_STEP',
      payload: {id: 1, stepType: 'transfer'}
    }
    expect(collapsedSteps(state, action)).toEqual({
      '1': false // default is false: not collapsed
    })
  })

  test('toggle step on->off', () => {
    const state = {
      '1': true,
      '2': false,
      '3': true,
      '4': true
    }
    const action = {
      type: 'TOGGLE_STEP_COLLAPSED',
      payload: 3
    }
    expect(collapsedSteps(state, action)).toEqual({
      '1': true,
      '2': false,
      '3': false,
      '4': true
    })
  })

  test('toggle step off-> on', () => {
    const state = {
      '1': true,
      '2': false,
      '3': true,
      '4': true
    }
    const action = {
      type: 'TOGGLE_STEP_COLLAPSED',
      payload: 2
    }
    expect(collapsedSteps(state, action)).toEqual({
      '1': true,
      '2': true,
      '3': true,
      '4': true
    })
  })
})

describe('orderedSteps reducer', () => {
  test('initial add step', () => {
    const state = []
    const action = {
      type: 'ADD_STEP',
      payload: {id: 123, stepType: 'transfer'}
    }
    expect(orderedSteps(state, action)).toEqual([123])
  })

  test('second add step', () => {
    const state = [123]
    const action = {
      type: 'ADD_STEP',
      payload: {id: 22, stepType: 'transfer'}
    }
    expect(orderedSteps(state, action)).toEqual([123, 22])
  })
})

describe('selectedStep reducer', () => {
  test('select step action: deselect with null', () => {
    const action = {
      type: 'SELECT_STEP',
      payload: null
    }
    expect(selectedStep(123, action)).toEqual(null)
    expect(selectedStep(null, action)).toEqual(null)
  })

  test('select step action: select by id', () => {
    const action = {
      type: 'SELECT_STEP',
      payload: 123
    }
    expect(selectedStep(5, action)).toEqual(123)
    expect(selectedStep(null, action)).toEqual(123)
  })
})

describe('stepCreationButtonExpanded reducer', () => {
  test('close (or stay closed) on newly added step', () => {
    const action = {
      type: 'ADD_STEP',
      payload: {id: 123, stepType: 'transfer'}
    }
    expect(stepCreationButtonExpanded(true, action)).toEqual(false)
    expect(stepCreationButtonExpanded(false, action)).toEqual(false)
  })

  test('update with EXPAND_ADD_STEP_BUTTON action payload', () => {
    expect(stepCreationButtonExpanded(false, {
      type: 'EXPAND_ADD_STEP_BUTTON',
      payload: true
    })).toEqual(true)

    expect(stepCreationButtonExpanded(true, {
      type: 'EXPAND_ADD_STEP_BUTTON',
      payload: false
    })).toEqual(false)
  })
})
