<!-- ArtivleList.vue -->

<template>
  <div class="article-list">
    <ArticleListItem v-for="article in filteredArticles" :key="article.id" :article="article" />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useArticleStore } from '@/stores/articles'
import ArticleListItem from '@/components/ArticleListItem.vue'

// ✅ 올바른 props 선언
const props = defineProps({
  selectedCategory: {
    type: Number,
    required: false,
    default: null
  }
})

const store = useArticleStore()

// ✅ 필터링된 게시글 목록
const filteredArticles = computed(() => {
  if (typeof props.selectedCategory === 'number') {
    return store.articles.filter(article => article.category === props.selectedCategory)
  }
  return store.articles
})
console.log('전체 articles:', store.articles)

</script>


<style scoped>
.article-list {
  display: flex;
  flex-direction: column;
  gap: 24px;
  min-height: 1500px;
  margin: 0 auto;
  padding: 48px 32px;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
  box-sizing: border-box;
}
</style>
