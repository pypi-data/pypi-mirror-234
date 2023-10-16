<template>
  <v-select
    v-bind="$attrs"
    :append-to-body="appendToBody"
    :class="[
      $style['ops-form-select'],
      { 'ops-form-select__error': hasErrors },
      { 'ops-form-select__position-top': position === 'top' },
      { 'ops-form-select__hide-values': hideValues }
    ]"
  >
    <template #open-indicator="{ attributes }">
      <div :class="[$style['ops-form-select__arrow-wrapper']]">
        <b v-bind="attributes" :class="[$style['ops-form-select__arrow']]" />
      </div>
    </template>
    <template #option="item">
      <slot name="select-option" v-bind="item" />
    </template>
    <template v-for="(_, name) in $slots" #[name]="slotData">
      <slot :name="name" v-bind="slotData" />
    </template>
  </v-select>
</template>
<script lang="ts" setup>
defineProps({
  hasErrors: {
    type: Boolean,
    default: false
  },
  hideValues: {
    type: Boolean,
    default: false
  },
  position: {
    type: String,
    default: ''
  },
  appendToBody: {
    type: Boolean,
    default: true
  }
})
</script>
<style lang="scss" module scoped>
.ops-form-select {
  @apply w-full cursor-pointer;
  &__arrow-wrapper {
    @apply absolute cursor-pointer h-full;
  }

  &__arrow {
    @apply border-solid mt-[-2px] cursor-pointer ml-[-4px] absolute w-0 top-1/2 left-1/2 h-0;
    border-color: #888 transparent transparent transparent;
    border-width: 5px 4px 0 4px;
  }
}
</style>
<style lang="scss">
.vs {
  &--single {
    &:is(.vs--open) {
      .vs__selected {
        opacity: 0 !important;
      }
    }
  }

  &--disabled {
    @apply rounded-full cursor-not-allowed #{!important};
  }

  &__dropdown {
    &-toggle {
      @apply text-[0.875rem] h-fit leading-6 text-grey-700  w-full border-grey-100 border-[0.0625rem] border-solid rounded-[0.5rem] min-h-[2.625rem] p-0 #{!important};
    }

    &-menu {
      @apply rounded-b-[0.5rem] max-h-[15rem] border-t py-0 border-solid text-base text-grey-900 font-normal #{!important};
    }

    &-option {
      @apply hover:bg-confetti-500 bg-white font-normal pl-4 text-[1rem] hover:text-grey-900  overflow-hidden truncate p-[6px] leading-6 font-normal #{!important};
      &--highlight {
        @apply bg-confetti-500 text-grey-900 #{!important};
      }
    }
  }

  &__deselect {
    @apply ml-2 #{!important};
  }

  &__selected {
    @apply pl-0 ml-0 mt-[1px] #{!important};
    &-options {
      @apply flex items-center py-0 px-[0.625rem] pl-[17px] w-[70%] lg:w-[90%] #{!important};
      input {
        &::placeholder {
          @apply text-base text-grey-200 font-medium #{!important};
        }
      }
    }

    @apply block truncate max-w-[90%] font-medium text-grey-950 text-[0.875rem]  #{!important};
  }

  &__spinner {
    @apply absolute rounded-[50%] right-[0.5rem] #{!important};
  }

  &__actions {
    @apply pr-[10px] #{!important};
  }

  &__clear {
    @apply absolute cursor-pointer z-50 leading-[2.5rem] top-[1.0625rem] text-[#888] mr-0 font-bold right-[1.25rem] #{!important};
  }
}

.v-select.ops-form-select__position-top:has(.vs__dropdown-menu) {
  .vs__dropdown-toggle {
    @apply rounded-t-none rounded-b-[0.5rem] h-fit  duration-500 #{!important};
  }
}

.v-select {
  &:is(.ops-form-select__position-top) {
    .vs__dropdown-menu {
      @apply top-auto rounded-t-[0.5rem] bottom-[calc(100%-1px)] shadow-none rounded-b-none #{!important};
    }
  }

  &:is(.ops-form-select__hide-values) {
    .vs__dropdown-toggle > .vs__selected-options > .vs__selected {
      display: none !important;
    }
  }

  &:has(.vs__dropdown-menu) {
    .vs__dropdown-toggle {
      @apply rounded-b-none h-fit  duration-500 #{!important};
    }
  }

  &:is(.vs--multiple) {
    .vs__selected {
      &-options {
        @apply flex items-center #{!important};
      }

      @apply block rounded-[0.5rem] cursor-pointer truncate max-w-[90%] border-grey-900 duration-500 font-bold text-white text-[0.875rem] bg-grey-900 py-[0.2rem] px-[0.5rem] #{!important};
      &:hover {
        @apply bg-confetti-500 border-transparent text-grey-900 #{!important};
        & > button > svg {
          @apply fill-grey-500 #{!important};
        }
      }

      & > button > svg {
        @apply fill-white #{!important};
      }
    }
  }
}

.ops-form-select__error {
  .vs__dropdown-toggle {
    @apply border-amaranth-900 #{!important};
  }
}
</style>
