<template>
  <div :class="[$style['mission-leg-wrapper']]">
    <div :class="[$style['mission-leg-wrapper__content']]">
      <AirportLocationAutocomplete
        v-model="missionFormModel.legs[legIndex].departure_location"
        :errors="errors?.departure_location"
        :is-validation-dirty="isValidationDirty"
        required
        label-text="Departure Airport:"
        @update:model-value="onChangeDepartureLocation"
      />
      <div class="flex flex-col mb-4 lg:mb-0">
        <div class="flex items-start gap-x-4 w-full">
          <div class="w-7/12">
            <ULabel required label-text="Departure Date:" />
            <UFlatPickr
              ref="departureDateRef"
              v-model="dateTime.departureDate"
              :errors="errors?.departure_datetime"
              :is-validation-dirty="isValidationDirty"
              placeholder="Select date"
              :config="{
                allowInput: true,
                altInput: true,
                altFormat: 'Y-m-d',
                dateFormat: 'Y-m-d',
                minDate: computedMinimumDepartureDate
              }"
              @on-change="(...args) => onChangeDepartureDate(args)"
              @on-close="onCloseCalendar"
            />
          </div>
          <div class="w-5/12">
            <ULabel required label-text="Time:" />
            <UFlatPickr
              v-model="dateTime.departureTime"
              placeholder="Time"
              :errors="errors?.departure_datetime"
              :is-validation-dirty="isValidationDirty"
              :config="{
                altFormat: 'H:i',
                altInput: true,
                allowInput: true,
                noCalendar: true,
                enableTime: true,
                time_24hr: true,
                minTime: computedMinimumDepartureTime,
                minuteIncrement: 1
              }"
              @on-change="(...args) => onChangeDepartureHours(args)"
              @on-close="onCloseCalendar"
            />
          </div>
          <div class="w-32">
            <ULabel :required="false" label-text="Timezone:" />
            <USelectWrapper
              :model-value="missionFormModel.legs[legIndex].departure_datetime_is_local"
              :options="[
                { label: 'UTC', value: false },
                { label: 'Local', value: true }
              ]"
              :reduce="(item) => item.value"
              :clearable="false"
              :disabled="!missionFormModel.legs[legIndex].departure_location?.is_lat_lon_available"
              label="label"
              placeholder="Timezone"
              class="timezone-select mb-0"
              :append-to-body="false"
              @update:model-value="onChangeTimeZone('departure_datetime_is_local', $event)"
            />
          </div>
        </div>
      </div>
      <AirportLocationAutocomplete
        v-model="missionFormModel.legs[legIndex].arrival_location"
        :errors="errors?.arrival_location"
        :is-validation-dirty="isValidationDirty"
        required
        label-text="Destination Airport:"
        @update:model-value="onChangeArrivalLocation"
      />
      <div class="flex flex-col mb-4 lg:mb-0">
        <div class="flex items-start gap-x-4">
          <div class="w-7/12">
            <ULabel required label-text="Arrival Date:" />
            <UFlatPickr
              v-model="dateTime.arrivalDate"
              placeholder="Select date"
              :errors="errors?.arrival_datetime"
              :is-validation-dirty="isValidationDirty"
              :config="{
                allowInput: true,
                altInput: true,
                altFormat: 'Y-m-d',
                dateFormat: 'Y-m-d',
                minDate: computeMinimumArrivalDate,
                minuteIncrement: 1
              }"
              @on-change="(...args) => onChangeArrivalDate(args)"
              @on-close="onCloseCalendar"
            />
          </div>
          <div class="w-5/12">
            <ULabel required label-text="Time:" />
            <UFlatPickr
              v-model="dateTime.arrivalTime"
              placeholder="Time"
              :errors="errors?.arrival_datetime"
              :is-validation-dirty="isValidationDirty"
              :config="{
                altFormat: 'H:i',
                altInput: true,
                allowInput: true,
                noCalendar: true,
                enableTime: true,
                time_24hr: true,
                minTime: computedMinimumArrivalTime,
                minuteIncrement: 1
              }"
              @on-change="(...args) => onChangeArrivalHours(args)"
              @on-close="onCloseCalendar"
            />
          </div>
          <div class="w-32">
            <ULabel :required="false" label-text="Timezone:" />
            <USelectWrapper
              :model-value="missionFormModel.legs[legIndex].arrival_datetime_is_local"
              :options="[
                { label: 'UTC', value: false },
                { label: 'Local', value: true }
              ]"
              :reduce="(item) => item.value"
              :clearable="false"
              :disabled="!missionFormModel.legs[legIndex].arrival_location?.is_lat_lon_available"
              label="label"
              placeholder="Timezone"
              class="timezone-select mb-0"
              :append-to-body="false"
              @update:model-value="onChangeTimeZone('arrival_datetime_is_local', $event)"
            />
          </div>
        </div>
      </div>
      <UInputWrapper
        v-model="missionFormModel.legs[legIndex].callsign_override"
        :errors="errors?.callsign_override"
        :is-validation-dirty="isValidationDirty"
        label-text="Callsign (if different):"
      />
      <UInputWrapper
        :model-value="missionFormModel.legs[legIndex].pob_crew"
        required
        type="number"
        :is-validation-dirty="isValidationDirty"
        label-text="Crew:"
        :errors="errors?.pob_crew"
        @update:model-value="onCrewUpdate"
      />
    </div>
  </div>
  <div class="flex mb-[18px]">
    <div class="flex px-[1.5rem] mt-[6px] gap-[1.5rem] w-full">
      <div class="flex w-1/2 flex-col">
        <div>
          <UCheckboxWrapper
            v-model="passengersCheckbox"
            label-text="Passengers?"
            @update:model-value="onHandleCheckBox($event, 'pob_pax')"
          />
          <UInputWrapper
            v-model="passengersQuantityComputed"
            type="number"
            :is-validation-dirty="isValidationDirty"
            :errors="errors?.pob_pax"
            :disabled="!passengersCheckbox"
          />
        </div>
      </div>
      <div class="flex w-1/2 flex-col">
        <div>
          <UCheckboxWrapper
            v-model="cargoCheckbox"
            label-text="Cargo? (lbs)"
            @update:model-value="onHandleCheckBox($event, 'cob_lbs')"
          />
          <UInputWrapper
            v-model="cargoQuantityComputed"
            type="number"
            :is-validation-dirty="isValidationDirty"
            :errors="errors?.cob_lbs"
            :disabled="!cargoCheckbox"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { computed, PropType, watch } from 'vue'
import UCheckboxWrapper from '@/components/ui/wrappers/UCheckboxWrapper.vue'
import UInputWrapper from '@/components/ui/wrappers/UInputWrapper.vue'
import { ErrorObject } from '@vuelidate/core'
import ULabel from '@/components/ui/form/ULabel.vue'
import AirportLocationAutocomplete from '@/components/autocomplete/AirportLocationAutocomplete.vue'
import type { ILegService, IMissionLegFormStructure } from '@/types/mission/mission.types'
import USelectWrapper from '@/components/ui/wrappers/USelectWrapper.vue'
import UFlatPickr from '@/components/ui/form/UFlatPickr/UFlatPickr.vue'
import { useMissionFormStore } from '@/stores/useMissionFormStore'
import { useMissionReferenceStore } from '@/stores/useMissionReferenceStore'
import { missionLegServiceDefaults } from '@/constants/mission.constants'
import { useMissionLegTime } from '@/composables/mission/mission-leg/useMissionLegTime'
import { useAirportLocation } from '@/composables/mission/mission-leg/useAirportLocation'
import { storeToRefs } from 'pinia'

const props = defineProps({
  legIndex: {
    type: Number,
    default: 0
  },
  isValidationDirty: {
    type: Boolean,
    default: false
  },
  errors: {
    type: Object as PropType<Record<string, ErrorObject[]>>,
    default: () => ({})
  }
})
const {
  dateTime,
  computedMinimumDepartureDate,
  computeMinimumArrivalDate,
  computedMinimumArrivalTime,
  computedMinimumDepartureTime,
  onCloseCalendar,
  onChangeDepartureDate,
  onChangeDepartureHours,
  onChangeArrivalDate,
  onChangeArrivalHours,
  onChangeTimeZone
} = useMissionLegTime(props.legIndex as number)

const { onChangeArrivalLocation, onChangeDepartureLocation } = useAirportLocation(
  props.legIndex as number
)

const missionFormStore = useMissionFormStore()
const missionsReferenceStore = useMissionReferenceStore()

const { selectedDestinationAirportsLeg, passengerService, cargoService } =
  storeToRefs(missionsReferenceStore)
const { formModel: missionFormModel } = storeToRefs(missionFormStore)

const passengersCheckbox = computed(() => {
  const prevLeg = missionFormModel.value?.legs?.[props.legIndex - 1]
  const currentLeg = missionFormModel.value?.legs?.[props.legIndex]

  return currentLeg?.arrival_aml_service || prevLeg?.arrival_aml_service
    ? isServiceSelected(passengerService.value?.id as number)
    : currentLeg?.pob_pax !== null
})

const passengersQuantityComputed = computed({
  get: () => missionFormModel.value?.legs?.[props.legIndex]?.pob_pax,
  set: (value: number) => {
    const leg = missionFormModel.value.legs[props.legIndex]
    if (+value < 0) return (leg.pob_pax = 0)
    leg.pob_pax = value
  }
})

const cargoCheckbox = computed(() => {
  const prevLeg = missionFormModel.value?.legs?.[props.legIndex - 1]
  const currentLeg = missionFormModel.value?.legs?.[props.legIndex]
  return currentLeg?.arrival_aml_service || prevLeg?.arrival_aml_service
    ? isServiceSelected(cargoService.value?.id)
    : currentLeg?.cob_lbs !== null
})

const cargoQuantityComputed = computed<number>({
  get: () => missionFormModel.value?.legs?.[props.legIndex]?.cob_lbs as number,
  set: (value: number) => {
    const leg = missionFormModel.value.legs?.[props.legIndex]
    if (!leg) return
    if (+value < 0) return (leg.cob_lbs = 0)
    leg.cob_lbs = value
  }
})

const isServiceSelected = (serviceId?: number): boolean => {
  if (!serviceId) return false
  const prevLeg = missionFormModel.value?.legs?.[props.legIndex - 1]
  const currentLeg = missionFormModel.value?.legs?.[props.legIndex]

  const isSelectedInPrevLeg = !!prevLeg?.servicing?.services?.find(
    (service) => service?.service === serviceId
  )?.on_departure
  const isSelectedInCurrentLeg = !!currentLeg?.servicing?.services?.find(
    (service) => service?.service === serviceId
  )?.on_arrival

  return isSelectedInPrevLeg || isSelectedInCurrentLeg
}

/** function handles leg Cargo & Passenger checkbox handling
 * @param flag - checkbox state
 * @param property - dependant on checkbox leg property
 * */
const onHandleCheckBox = (
  flag: boolean,
  property: keyof Pick<IMissionLegFormStructure, 'pob_pax' | 'cob_lbs'>
) => {
  const currLeg = missionFormModel.value?.legs?.[props.legIndex]
  onHandleLegServicing(
    flag,
    property === 'pob_pax' ? passengerService.value?.id : cargoService.value?.id
  )
  currLeg && (currLeg[property] = flag ? 0 : null)
}

/** function handles leg additional servicing dependant on passenger & cargo checkboxes
 * @param flag - checkbox state
 * @param service - dependant service id (passenger_handling / cargo_handling) get from reference store
 */
const onHandleLegServicing = (flag: boolean, service?: number) => {
  // Do not handle if service is missing
  if (!service) return
  const prevLeg = missionFormModel.value?.legs?.[props.legIndex - 1]
  const currentLeg = missionFormModel.value?.legs?.[props.legIndex]
  const handleService = (
    leg: IMissionLegFormStructure,
    servicingType: 'on_departure' | 'on_arrival'
  ) => {
    if (!leg.servicing?.services) return
    const serviceIndex = (leg?.servicing?.services as ILegService[])?.findIndex(
      (item) => item?.service === service
    )
    const oppositeServicingType = servicingType === 'on_departure' ? 'on_arrival' : 'on_departure'
    // Add service if it is not present
    if (serviceIndex < 0) {
      flag &&
        leg.servicing.services.push({
          ...missionLegServiceDefaults(service),
          [servicingType]: true
        })
      return
    }
    // Remove service if not used
    if (!leg.servicing.services?.[serviceIndex]?.[oppositeServicingType] && !flag) {
      return leg.servicing.services.splice(serviceIndex, 1)
    }
    // Update service flag
    return (leg.servicing.services[serviceIndex] = {
      ...(leg.servicing.services[serviceIndex] as ILegService),
      [servicingType]: flag
    })
  }

  if (prevLeg?.arrival_aml_service && prevLeg?.servicing && prevLeg?.servicing?.services) {
    handleService(prevLeg, 'on_departure')
  }
  if (currentLeg?.arrival_aml_service && currentLeg?.servicing && currentLeg?.servicing?.services) {
    handleService(currentLeg, 'on_arrival')
  }
}

/** function adds automatical services based on cargo & passenger checkboxes
 */
const handleAutomaticalServices = () => {
  const currentLeg = missionFormModel.value?.legs?.[props.legIndex]
  const nextLeg = missionFormModel.value?.legs?.[props.legIndex + 1]

  const addOrUpdateService = (
    serviceId: number | undefined,
    servicingType: 'on_departure' | 'on_arrival'
  ) => {
    if (!currentLeg.servicing?.services) return

    const serviceIndex = (currentLeg?.servicing?.services as ILegService[])?.findIndex(
      (item) => item?.service === serviceId
    )
    serviceIndex > -1
      ? (currentLeg.servicing.services[serviceIndex] = {
          ...currentLeg.servicing.services[serviceIndex],
          [servicingType]: true
        } as ILegService)
      : currentLeg.servicing?.services?.push({
          ...missionLegServiceDefaults(serviceId as number),
          [servicingType]: true
        })
  }
  if (currentLeg?.cob_lbs !== null) {
    addOrUpdateService(cargoService.value?.id, 'on_arrival')
  }
  if (currentLeg?.pob_pax !== null) {
    addOrUpdateService(passengerService.value?.id, 'on_arrival')
  }
  if (nextLeg?.cob_lbs !== null) {
    addOrUpdateService(cargoService.value?.id, 'on_departure')
  }
  if (nextLeg?.pob_pax !== null) {
    addOrUpdateService(passengerService.value?.id, 'on_departure')
  }
}

const onCrewUpdate = (value) => {
  missionFormModel.value.legs[props.legIndex].pob_crew = value

  if (missionFormModel.value.legs.length) {
    missionFormModel.value.legs = missionFormModel.value.legs.map((el, index) =>
      index <= props.legIndex ? el : { ...el, pob_crew: value }
    )
  }
}

watch(passengersCheckbox, (flag) => {
  const currLeg = missionFormModel.value?.legs?.[props.legIndex]
  if (!flag) currLeg.pob_pax = null
  else if (flag && missionFormModel.value.legs[props.legIndex].pob_pax === null) currLeg.pob_pax = 0
})

watch(cargoCheckbox, (flag) => {
  const currLeg = missionFormModel.value?.legs?.[props.legIndex]
  if (!flag) currLeg.cob_lbs = null
  else if (flag && missionFormModel.value.legs[props.legIndex].cob_lbs === null) currLeg.cob_lbs = 0
})

watch(
  () => missionFormModel.value?.legs?.[props.legIndex]?.arrival_aml_service,
  (isAmlServiceSelected) => {
    if (isAmlServiceSelected) {
      handleAutomaticalServices()
    }
  }
)

watch(
  () => missionFormModel.value.legs[props.legIndex]?.arrival_location,
  (location) => {
    if (location?.id) selectedDestinationAirportsLeg.value[props.legIndex] = location
  }
)
</script>

<style lang="scss" module>
.mission-leg-wrapper {
  @apply relative flex flex-col bg-white min-w-0 rounded-[0.5rem];

  &__content {
    @apply grid px-6 gap-x-[1.5rem] gap-y-[2.5px] mt-4  grid-cols-1 lg:grid-cols-2 font-medium text-[1.25rem] text-grey-900;
  }
}
</style>
<style lang="scss">
.timezone-select {
  .vs__dropdown-menu {
    @apply min-w-[5rem] #{!important};
  }
}
</style>
