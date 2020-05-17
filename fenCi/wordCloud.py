from wordcloud import WordCloud
import matplotlib.pyplot as plt
import  pkuFenci

# 生成词云
def create_word_cloud(frequencies, filename, encoding, font_path):
    wc = WordCloud(
        font_path=font_path,
        max_words=100,
        width=2000,
        height=1200,
    )
    word_cloud = wc.generate_from_frequencies(frequencies)
    # 写词云图片
    word_cloud.to_file("wordcloud.jpg")
    # 显示词云文件
    plt.imshow(word_cloud)
    plt.axis("off")
    plt.show()

if __name__ == '__main__':
    dict = pkuFenci.get_dict()
    create_word_cloud(dict,"./record.txt","utf-8","C:\WINDOWS\FONTS\STKAITI.TTF")