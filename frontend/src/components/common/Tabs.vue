<script setup>
import { TabGroup, TabList, Tab, TabPanels, TabPanel } from '@headlessui/vue'

const props = defineProps({
  tabs: {
    type: Array,
    required: true
    // Expected format: [{ key: 'daily', label: '每日热门' }, ...]
  },
  modelValue: {
    type: [String, Number],
    required: true
  }
})

const emit = defineEmits(['update:modelValue'])

const getCurrentTabIndex = () => {
  return props.tabs.findIndex(tab => tab.key === props.modelValue)
}

const handleTabChange = (index) => {
  const selectedTab = props.tabs[index]
  if (selectedTab) {
    emit('update:modelValue', selectedTab.key)
  }
}
</script>

<template>
  <TabGroup :selected-index="getCurrentTabIndex()" @change="handleTabChange">
    <TabList class="flex space-x-1 border-b border-border-color">
      <Tab
        v-for="tab in tabs"
        :key="tab.key"
        v-slot="{ selected }"
        as="template"
      >
        <button
          :class="[
            'px-4 py-2 text-base font-medium transition-colors duration-200 focus:outline-none',
            'border-b-2 -mb-px',
            selected
              ? 'border-accent text-accent font-semibold'
              : 'border-transparent text-text-secondary hover:text-text-primary hover:border-gray-300'
          ]"
        >
          {{ tab.label }}
        </button>
      </Tab>
    </TabList>

    <TabPanels class="mt-4">
      <TabPanel
        v-for="tab in tabs"
        :key="tab.key"
        class="focus:outline-none"
      >
        <slot :name="tab.key"></slot>
      </TabPanel>
    </TabPanels>
  </TabGroup>
</template>
