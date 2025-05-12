<template>
    <section class="features">
        <div class="container">
            <h2 class="section-title">核心功能</h2>
            <div class="features-grid">
                <div class="feature-card">
                    <div class="icon">🤖</div>
                    <h3>自动交易</h3>
                    <p>部署毫秒级响应的交易机器人，24/7监控市场，执行复杂策略，性能远超人类极限。</p>
                </div>
                <div class="feature-card">
                    <div class="icon">👥</div>
                    <h3>社交交易</h3>
                    <p>一键跟单顶级交易员，或订阅、购买经过验证的策略模板，轻松复制成功经验。</p>
                </div>
                <div class="feature-card">
                    <div class="icon">🛠️</div>
                    <h3>专业工具</h3>
                    <p>提供模拟交易、历史数据回测、可视化策略设计器等强大工具，助您验证和优化策略。</p>
                </div>
            </div>
        </div>
    </section>
</template>

<script>
export default {
    name: 'FeaturesComponent'
}
</script>

<style scoped>
.features {
    padding: 80px 0;
    background-color: var(--bg-light);
}
.section-title {
    text-align: center;
    font-size: 36px;
    margin-bottom: 48px;
}
.features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 32px;
}
.feature-card {
    background-color: var(--bg-dark);
    padding: 32px;
    border-radius: 12px;
    border: 1px solid var(--border-color);
    text-align: center;
    transition: transform 0.3s, box-shadow 0.3s;
}
.feature-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 20px 40px rgba(0, 243, 255, 0.1);
}
.feature-card .icon {
    font-size: 48px;
    color: var(--accent-color);
    margin-bottom: 16px;
}
.feature-card h3 {
    font-size: 24px;
    margin-bottom: 12px;
}
.feature-card p {
    color: var(--text-secondary);
    line-height: 1.6;
}
</style>