<template>
  <div ref="parentRef">
    <VueDatePicker
      v-bind="$attrs"
      ref="calendar"
      v-model="dateValue"
      :placeholder="placeholder"
      :class="{ 'ops-calendar__error': hasErrors && isValidationDirty }"
      :month-change-on-scroll="false"
      format="yyyy-MM-dd, HH:mm"
      :flow="['calendar', 'time']"
      partial-flow
      :close-on-auto-apply="false"
      auto-apply
      hide-input-icon
      inline-with-input
      text-input
      no-hours-overlay
      no-minutes-overlay
      :min-date="minDate"
      :min-time="minTime"
      @focus="onClickCalendar"
      @time-picker-open="onTimePickerOpen"
      @cleared="onClearTimePicker"
      @update:model-value="onChangeDateValue"
    >
      <template #calendar-header="{ day }">
        {{ day[0] }}
      </template>
      <template #dp-input="data">
        <input
          placeholder="Select a date"
          class="dp__input"
          type="text"
          :value="formatDate(dateValue)"
          v-bind="data"
          @click="onClickSelectDate"
        />
      </template>
    </VueDatePicker>
    <p v-if="errors?.length && isValidationDirty" :class="[$style['ops-calendar__error']]">
      <span v-for="(error, index) in errors" :key="`${index}_${error.$property}`">
        {{ index === 0 ? error.$message : '' }}
      </span>
    </p>
  </div>
</template>
<script setup lang="ts">
import { computed, onMounted, onUpdated, PropType, ref, watch } from 'vue'
import dayjs from 'dayjs'
import { ErrorObject } from '@vuelidate/core'
import utc from 'dayjs/plugin/utc'
import timezone from 'dayjs/plugin/timezone'

dayjs.extend(utc)
dayjs.extend(timezone)
const props = defineProps({
  errors: {
    type: Array as PropType<ErrorObject[] | string>,
    default: () => []
  },
  placeholder: {
    type: String,
    default: 'Select a date'
  },
  isValidationDirty: {
    type: Boolean,
    default: false
  },
  modelValue: {
    type: [String, Date, Number],
    default: () => null
  },
  minDate: {
    type: [String, Date, Number, Object],
    default: () => null
  },
  minTime: {
    type: [String, Date, Number, Object],
    default: () => null
  }
})
const emit = defineEmits(['update:model-value'])
const calendar = ref()
const parentRef = ref<HTMLDivElement>()
const isSameDates = (date1: Date, date2: Date) => {
  const dayDate1 = dayjs(date1)
  const dayDate2 = dayjs(date2)
  return (
    dayDate1.hour() === dayDate2.hour() &&
    dayDate1.date() === dayDate2.date() &&
    dayDate1.month() === dayDate2.month() &&
    dayDate1.year() === dayDate2.year()
  )
}
const changeDateValue = (value: Date | string | number) => {
  const button = parentRef.value?.querySelector(
    '.dp__time_col:first-child .dp__btn:not(.dp__inc_dec_button)'
  ) as HTMLButtonElement
  const buttonsDecInc = parentRef.value?.querySelectorAll(
    '.dp__time_col:first-child .dp__btn.dp__inc_dec_button'
  )
  const clonedButtonsIncDec = parentRef.value?.querySelectorAll('.dp__inc_dec_btn-custom')
  if (buttonsDecInc && clonedButtonsIncDec?.length === 0) {
    Array.from(buttonsDecInc).forEach((btn) => {
      btn?.removeAttribute('disabled')
      btn?.classList.add('dp__inc_dec_btn-custom')
      btn?.classList.remove('dp__inc_dec_button_disabled')
      const cloneButton = btn.cloneNode() as HTMLButtonElement
      cloneButton.innerHTML = btn.innerHTML
      ;(btn as HTMLButtonElement).style.display = 'none'
      btn.insertAdjacentElement('afterend', cloneButton)
      btn.remove()
    })
    const clonedButtonIncDec = parentRef.value?.querySelectorAll(
      '.dp__inc_dec_btn-custom'
    ) as NodeListOf<HTMLButtonElement>
    const buttonInc = clonedButtonIncDec[0]
    const buttonDec = clonedButtonIncDec[1]
    const dateBefore = new Date(dateValue.value || new Date().toString())
    const hoursBefore = dateBefore.getHours()
    const minDateHours = props.minDate ? new Date(props.minDate as Date).getHours() : 0
    buttonDec.classList.remove('dp__inc_dec_button_disabled')
    buttonInc.classList.remove('dp__inc_dec_button_disabled')
    buttonDec.classList.remove('dp__inc_dec_button--disabled')
    buttonInc.classList.remove('dp__inc_dec_button--disabled')
    buttonInc.removeAttribute('disabled')
    buttonDec.removeAttribute('disabled')
    if (
      hoursBefore - 1 <= minDateHours &&
      (dayjs(dateBefore).isSame(props.minDate as Date) ||
        dayjs(dateBefore).isBefore(props.minDate as Date))
    ) {
      buttonDec.classList.add('dp__inc_dec_button_disabled')
      buttonDec.classList.add('dp__inc_dec_button--disabled')
      buttonDec.setAttribute('disabled', 'true')
    } else if (hoursBefore >= 23) {
      buttonInc.classList.add('dp__inc_dec_button_disabled')
      buttonInc.classList.add('dp__inc_dec_button--disabled')
      buttonInc.setAttribute('disabled', 'true')
    } else if (dateBefore.getHours() >= 23) {
      buttonInc.classList.add('dp__inc_dec_button_disabled')
      buttonInc.classList.add('dp__inc_dec_button--disabled')
      buttonInc.setAttribute('disabled', 'true')
    } else {
      buttonDec.classList.remove('dp__inc_dec_button_disabled')
      buttonInc.classList.remove('dp__inc_dec_button_disabled')
      buttonDec.classList.remove('dp__inc_dec_button--disabled')
      buttonInc.classList.remove('dp__inc_dec_button--disabled')
      buttonInc.removeAttribute('disabled')
      buttonDec.removeAttribute('disabled')
    }
    buttonInc?.addEventListener('click', () => {
      const customButton = parentRef.value?.querySelector('.dp__btn-custom') as
        | HTMLButtonElement
        | undefined
      const hoursBefore = new Date(dateValue.value || new Date().toString()).getHours()
      const currentDate = dayjs(dateValue.value || new Date())
        .add(1, 'hour')
        .toDate()
      buttonDec.classList.remove('dp__inc_dec_button_disabled')
      buttonInc.classList.remove('dp__inc_dec_button_disabled')
      buttonDec.classList.remove('dp__inc_dec_button--disabled')
      buttonInc.classList.remove('dp__inc_dec_button--disabled')
      buttonInc.removeAttribute('disabled')
      buttonDec.removeAttribute('disabled')
      if (hoursBefore - 1 <= minDateHours && isSameDates(currentDate, props.minDate as Date)) {
        buttonDec.classList.add('dp__inc_dec_button_disabled')
        buttonDec.classList.add('dp__inc_dec_button--disabled')
        buttonDec.setAttribute('disabled', 'true')
      } else if (hoursBefore >= 23) {
        buttonInc.classList.add('dp__inc_dec_button_disabled')
        buttonInc.classList.add('dp__inc_dec_button--disabled')
        buttonInc.setAttribute('disabled', 'true')
      } else if (hoursBefore + 1 >= 23) {
        buttonInc.classList.add('dp__inc_dec_button_disabled')
        buttonInc.classList.add('dp__inc_dec_button--disabled')
        buttonInc.setAttribute('disabled', 'true')
      } else {
        buttonDec.classList.remove('dp__inc_dec_button_disabled')
        buttonInc.classList.remove('dp__inc_dec_button_disabled')
        buttonDec.classList.remove('dp__inc_dec_button--disabled')
        buttonInc.classList.remove('dp__inc_dec_button--disabled')
        buttonInc.removeAttribute('disabled')
        buttonDec.removeAttribute('disabled')
      }
      if (hoursBefore < 23) {
        emit('update:model-value', currentDate.toString())
        if (customButton) {
          customButton.textContent = currentDate.getHours().toString()
        }
      } else {
        buttonInc.classList.add('dp__inc_dec_button_disabled')
        buttonInc.classList.add('dp__inc_dec_button--disabled')
        buttonInc.setAttribute('disabled', 'true')
      }
    })
    buttonDec?.addEventListener('click', () => {
      const customButton = parentRef.value?.querySelector('.dp__btn-custom') as
        | HTMLButtonElement
        | undefined
      const dateBefore = new Date(dateValue.value || new Date().toString())
      const hoursBefore = dateBefore.getHours()
      const currentDate = dayjs(dateValue.value || new Date())
        .subtract(1, 'hour')
        .toDate()
      buttonDec.classList.remove('dp__inc_dec_button_disabled')
      buttonInc.classList.remove('dp__inc_dec_button_disabled')
      buttonDec.classList.remove('dp__inc_dec_button--disabled')
      buttonInc.classList.remove('dp__inc_dec_button--disabled')
      buttonInc.removeAttribute('disabled')
      buttonDec.removeAttribute('disabled')
      if (hoursBefore - 1 <= minDateHours && isSameDates(currentDate, props.minDate as Date)) {
        buttonDec.classList.add('dp__inc_dec_button_disabled')
        buttonDec.classList.add('dp__inc_dec_button--disabled')
        buttonDec.setAttribute('disabled', 'true')
      } else if (hoursBefore >= 23) {
        buttonInc.classList.add('dp__inc_dec_button_disabled')
        buttonInc.classList.add('dp__inc_dec_button--disabled')
        buttonInc.setAttribute('disabled', 'true')
      } else if (hoursBefore - 1 >= 23) {
        buttonInc.classList.add('dp__inc_dec_button_disabled')
        buttonInc.classList.add('dp__inc_dec_button--disabled')
        buttonInc.setAttribute('disabled', 'true')
      } else {
        buttonDec.classList.remove('dp__inc_dec_button_disabled')
        buttonInc.classList.remove('dp__inc_dec_button_disabled')
        buttonDec.classList.remove('dp__inc_dec_button--disabled')
        buttonInc.classList.remove('dp__inc_dec_button--disabled')
        buttonInc.removeAttribute('disabled')
        buttonDec.removeAttribute('disabled')
      }
      if (
        hoursBefore > 0 &&
        (!dayjs(currentDate).isBefore(props.minDate as Date) ||
          dayjs(currentDate).isSame(props.minDate as Date))
      ) {
        emit('update:model-value', currentDate.toString())
        if (customButton) {
          customButton.textContent = currentDate.getHours().toString()
        }
      } else {
        buttonDec.classList.add('dp__inc_dec_button_disabled')
        buttonDec.classList.add('dp__inc_dec_button--disabled')
        buttonDec.setAttribute('disabled', 'true')
      }
    })
  }
  if (button) {
    let computedValue = value
    if (props.minDate && dayjs(value).isBefore(props.minDate as Date)) {
      computedValue = props.minDate as Date
    } else if (!value && props.minDate) {
      computedValue = props.minDate as Date
    }
    if (computedValue) {
      emit('update:model-value', computedValue.toString())
      return
    }
    const utcDate = computedValue ? new Date(computedValue) : new Date()
    if (!computedValue) {
      utcDate.setHours(utcDate.getUTCHours())
    }
    const utcHour = utcDate.getHours().toString()
    const cloneButton = button.cloneNode(true) as HTMLButtonElement
    cloneButton.textContent = utcHour
    cloneButton.classList.add('dp__btn-custom')
    button.insertAdjacentElement('afterend', cloneButton)
    if (!value) {
      emit('update:model-value', utcDate.toString())
    }
    cloneButton.textContent = utcHour.toString()
    button.style.display = 'none'
  }
}
const formatDate = (value: Date | string | number) => {
  if (!value) return ''
  return dayjs(value).format('YYYY-MM-DD, HH:mm')
}
const dateValue = computed({
  get: () => props.modelValue,
  set: (value) => {
    if (!props.minDate && !props.modelValue) {
      const computedDate = new Date(value)
      computedDate.setHours(computedDate.getUTCHours())
      emit('update:model-value', value ? computedDate.toString() : '')
    } else {
      emit('update:model-value', new Date(value).toString())
    }
  }
})
const onTimePickerOpen = () => {
  setTimeout(() => {
    changeDateValue(dateValue.value)
  }, 50)
}
const onChangeDateValue = (value: Date | string | number) => {
  let computedValue = value
  if (props.minDate && dayjs(value).isBefore(props.minDate as Date)) {
    computedValue = props.minDate as Date
  } else if (!value && props.minDate) {
    computedValue = props.minDate as Date
  }
  const utcDate = computedValue ? new Date(computedValue) : new Date()
  if (!dateValue.value) {
    utcDate.setHours(utcDate.getUTCHours())
  }
  emit('update:model-value', utcDate.toString())
}
watch(
  () => props.minDate,
  () => {
    onChangeDateValue(dateValue.value)
  }
)
const onClearTimePicker = () => {
  emit('update:model-value', null)
}
const onClickSelectDate = () => {
  calendar.value?.openMenu()
}
const hasErrors = computed(() => {
  return props.errors?.length || typeof props.errors === 'string'
})
const onClickCalendar = () => {
  calendar.value?.openMenu()
}
defineExpose({
  calendar
})
</script>
<style lang="scss" module>
.ops-calendar {
  &__error {
    @apply text-amaranth-900  -bottom-8 lg:-bottom-4 text-xs;
  }
}
</style>
<style lang="scss">
@import '@vuepic/vue-datepicker/dist/main.css';

.ops-calendar__error {
  .dp__input {
    @apply border-amaranth-900 #{!important};
  }
}

.dp {
  &__input {
    @apply pr-8 pl-4 leading-6 w-full border-grey-100 border-[0.0625rem] border-solid rounded-[0.5rem] h-[2.625rem] text-grey-950 text-[0.875rem] font-medium #{!important};
    &::placeholder {
      @apply text-grey-200 text-base font-medium #{!important};
    }
  }

  &__time_picker_inline_container {
    @apply pb-4;
  }

  &__inc_dec_button_disabled,
  &__inc_dec_button--disabled {
    @apply cursor-not-allowed #{!important};
  }
}
</style>
<style>
:root {
  --dp-border-radius: 8px;
  --dp-cell-border-radius: 50%;
  --dp-button-heigh: 28px;
  --dp-cell-size: 28px;
  --dp-menu-min-width: 250px;
  --dp-font-size: 14px;
}

.dp__theme_light {
  --dp-hover-icon-color: #959595;
  --dp-primary-color: #515d8a;
}
</style>
