function initializeEmojiShow(emojiShow) {
    const src = emojiShow.getAttribute('src');
    if (src) {
        // 创建卡片容器
        const card = document.createElement('div');
        card.className = 'card';
        card.style.width = '18rem';
        card.style.overflow = 'hidden'; // 确保内容不溢出

        // 创建图片元素
        const img = document.createElement('img');
        img.className = 'card-img-top';
        img.alt = 'Emoji Image';
        img.src = new URL(src, window.location.href).href;
        card.appendChild(img);

        // 创建卡片主体
        const cardBody = document.createElement('div');
        cardBody.className = 'card-footer text-body-secondary';

        // 创建 URI 文本元素
        const uriText = document.createElement('p');
        uriText.className = 'card-text';
        const imgSrc = img.src;
        uriText.textContent = imgSrc;
        uriText.style.cursor = 'pointer';
        cardBody.appendChild(uriText);

        // 将卡片主体添加到卡片
        card.appendChild(cardBody);

        // 将卡片添加到 emojiShow
        emojiShow.appendChild(card);

        // 添加点击事件监听器以复制 URI 到剪贴板
        uriText.addEventListener('click', () => {
            copyToClipboard(imgSrc);
            showTooltip(uriText, 'Copied to clipboard');
        });
    }
}

function copyToClipboard(text) {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    document.body.removeChild(textarea);
}

function showTooltip(element, message) {
    const tooltip = document.createElement('div');
    tooltip.textContent = message;
    tooltip.style.position = 'absolute';
    tooltip.style.backgroundColor = '#000';
    tooltip.style.color = '#fff';
    tooltip.style.padding = '5px';
    tooltip.style.borderRadius = '5px';
    tooltip.style.top = `${element.offsetTop - 30}px`;
    tooltip.style.left = `${element.offsetLeft}px`;
    tooltip.style.zIndex = '1000';
    element.appendChild(tooltip);

    setTimeout(() => {
        element.removeChild(tooltip);
    }, 2000);
}