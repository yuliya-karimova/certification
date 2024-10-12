<template>
  <div class="max-w-screen-xl w-full flex flex-col gap-20">
    <!-- главная -->
    <div
      class="flex flex-col sm:flex-row items-center gap-6 lg:gap-12 font-mont max-sm:text-center"
    >
      <div class="flex-1">
        <div class="text-lg sm:text-2xl lg:text-3xl uppercase">Автоматизация</div>
        <h1 class="font-bold text-4xl sm:text-5xl md:text-6xl uppercase">проверки требований</h1>
        <div class="text-xl lg:text-2xl">в сертифицируемом контуре</div>
      </div>
      <div>
        <img alt="home pic" class="w-full h-auto" src="/auto.png" />
      </div>
    </div>

    <!-- анализ -->
    <div class="flex flex-col gap-4">
      <h2 class="text-xl md:text-3xl text-primary-800 font-mont">
        Введите текст требования для проверки:
      </h2>
      <BaseTextarea
        v-model="requirement"
        placeholder="Текст требования"
        class="w-full text-left"
        name="description"
        rows="10"
      />
      <!-- <div class="mb-12">
        <BaseButton theme="primary" @click="checkUseCase"> Проверить корректность </BaseButton>
      </div> -->

      <!-- временный блок -->
      <div class="flex items-center gap-4 flex-wrap">
        <BaseButton theme="primary" @click="checkUseCase"> Проверить корректность </BaseButton>

        <BaseButton theme="primary" @click="checkObjects">
          Проверить наличие объектов, подлежащих сертифицированию
        </BaseButton>

        <BaseButton theme="primary" @click="checkRegulations">
          Проверить соответствие регламентам
        </BaseButton>
      </div>
      <!-- временный блок -->

      <!-- результаты -->
      <div class="flex flex-col gap-24">
        <div v-if="checkResult.useCase">
          <div class="text-3xl font-bold text-accent-500 mb-6">Проверка на корректность</div>
          <MarkdownBlock :content="checkResult.useCase" />
          <!-- <div class="mt-12">
            <BaseButton theme="primary" @click="checkObjects">
              Проверить наличие объектов, подлежащих сертифицированию
            </BaseButton>
          </div> -->
        </div>

        <div v-if="checkResult.objects">
          <div class="text-3xl font-bold text-accent-500">
            Наличие объектов, подлежащих сертифицированию
          </div>
          <MarkdownBlock :content="checkResult.objects" />
          <!-- <div class="mt-12">
            <BaseButton theme="primary" @click="checkRegulations">
              Проверить соответствие регламентам
            </BaseButton>
          </div> -->
        </div>

        <div v-if="checkResult.regulations">
          <div class="text-3xl font-bold text-accent-500">Соответствие регламентам</div>
          <MarkdownBlock :content="checkResult.regulations" />
        </div>
        <div v-if="isChecking" class="flex gap-6 items-center">
          <BaseSpinner />
          <div>{{ checkingText }}</div>
        </div>
      </div>
    </div>

    <!-- уточнения? -->
    <!-- <div class="flex flex-col gap-4" v-if="checkResult">
      <h2 class="text-xl md:text-3xl text-primary-800 font-mont">Есть уточнения?</h2>
      <div class="flex flex-col gap-4">
        <div v-for="(item, index) in dialog" :key="index">
          <span class="font-bold">{{ `${item.role}: ` }}</span>
          <span>{{ item.content }}</span>
        </div>
        <BaseTextarea
          v-model="dialogNewMessage"
          placeholder="Задай вопрос"
          class="w-full text-left"
          name="description"
          rows="5"
        />
        <div>
          <BaseButton theme="secondary" @click="correct"> Уточнить </BaseButton>
        </div>
        <div v-if="isDialogLoading">
          <BaseSpinner />
        </div>
      </div>
    </div> -->
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useCheckStore } from '@/stores/check'
import BaseSpinner from '@/components/base/BaseSpinner.vue'
import BaseTextarea from '@/components/base/BaseTextarea.vue'
import BaseButton from '@/components/base/button/BaseButton.vue'
import MarkdownBlock from '@/components/MarkdownBlock.vue'
// import { DialogItem } from '@/models/dialog'

const requirement = ref('')
// const checkDialog = ref<DialogItem[]>([])

const isChecking = ref<boolean>(false)
const checkingText = ref('')
const checkResult = reactive({
  useCase: '',
  objects: '',
  regulations: ''
})

const checkStore = useCheckStore()

const checkUseCase = async () => {
  isChecking.value = true
  checkingText.value = 'Проверяем use case на корректность'

  const response = await checkStore.checkUseCase(requirement.value)

  checkResult.useCase = response
  isChecking.value = false
}

const checkObjects = async () => {
  isChecking.value = true
  checkingText.value = 'Проверяем наличие объектов, подлежащих сертифицированию'

  const response = await checkStore.checkObjects(requirement.value)

  checkResult.objects = response
  isChecking.value = false
}

const checkRegulations = async () => {
  isChecking.value = true
  checkingText.value = 'Проверяем соответстврие регламентам'

  const response = await checkStore.checkRegulations(requirement.value)

  checkResult.regulations = response
  isChecking.value = false
}

// const dialog = ref<DialogItem[]>([])
// const isDialogLoading = ref<boolean>(false)
// const dialogNewMessage = ref('')

// const checkRequirement = async () => {
//   isUseCaseChecking.value = true

//   checkDialog.value.push({ role: 'user', content: requirement.value })

//   const response = await checkStore.check(checkDialog.value)

//   checkDialog.value.push({ role: 'system', content: response })

//   checkResult.value = response
//   isUseCaseChecking.value = false
// }

// const correct = async () => {
//   isDialogLoading.value = true

//   dialog.value.push({ role: 'user', content: dialogNewMessage.value })

//   const response = await reportStore.correct([...checkDialog.value, ...dialog.value])

//   dialog.value.push({role: 'system', content: response })

//   isDialogLoading.value = false
//   dialogNewMessage.value = ''
// }
</script>
