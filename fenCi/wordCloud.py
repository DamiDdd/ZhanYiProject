from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
import  pkuFenci

# 生成词云
def create_word_cloud(frequencies, font_path, mask_image):
    mask = plt.imread(mask_image)
    wc = WordCloud(
        font_path=font_path,
        max_words=100,
        width=2000,
        height=1200,
        background_color="white",
        mask=mask,
    )
    word_cloud = wc.generate_from_frequencies(frequencies)
    word_cloud.recolor(color_func=ImageColorGenerator(mask))
    # 写词云图片
    word_cloud.to_file("wordcloud.jpg")
    # 显示词云文件
    plt.imshow(word_cloud)
    plt.axis("off")
    plt.show()

if __name__ == '__main__':
    dict = pkuFenci.get_dict()
    create_word_cloud(dict,"C:\WINDOWS\FONTS\STKAITI.TTF", "./mask.jpg")