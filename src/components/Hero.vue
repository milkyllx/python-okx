<template>
    <section class="hero">
        <div class="container">
            <h1>最智能的加密货币交易平台</h1>
            <p>专为追求极致性能的交易者打造。提供自动交易、社交跟单、专业级分析工具，助您在市场中占尽先机。</p>
            <div>
                <a href="#" class="btn btn-primary">立即注册 →</a>
                <a href="#" class="btn btn-outline">► 观看介绍视频</a>
            </div>
        </div>
    </section>
</template>

<script>
export default {
    name: 'HeroComponent'
}
</script>

<style scoped>
.hero {
    text-align: center;
    padding: 120px 0;
    background: linear-gradient(rgba(18, 21, 28, 0.8), rgba(18, 21, 28, 0.8)), url('../assets/images/hero-bg.jpg') no-repeat center center/cover;
}
.hero h1 {
    font-size: 56px;
    margin-bottom: 16px;
}
.hero p {
    font-size: 18px;
    color: var(--text-secondary);
    max-width: 600px;
    margin: 0 auto 32px;
}
.hero .btn {
    padding: 16px 32px;
    font-size: 18px;
}
</style>