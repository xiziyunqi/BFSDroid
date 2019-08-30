BFSDroid：基于特征融合和GBDT算法的Android恶意软件检测系统
注意：运行此代码需要安装AndroGuard。以下是每个文件的简介：
对比实验结果.html ：对比实验的代码和实验结果
验证实验结果_BFSDroid.html ：BFSDroid的验证实验代码和实验结果
验证实验结果_Maldetect.html ：Maldetect的验证实验的代码和实验结果
extract_write_opcode.py ：提取APK文件的3-Gram Dalvik操作码特征，并将结果写成一个csv文件
extract_write_permission.py ：提取APK文件的权限特征，并将结果写成一个csv文件
ben_permission_4000.csv : 对比实验提取的正常样本的权限特征，共1978个
ben_data_opcode_4000.csv ： 对比实验提取的正常样本的Dalvik操作码特征，共1978个
mal_data_opcode_4000.csv ： 提取的恶意样本3-Gram Dalvik操作码特征，共1987个
mal_permission_4000.csv ： 提取的恶意样本权限特征，共1987个####
google_ben_opcode.csv ：验证实验提取的Google Play样本3-Gram Dalvik操作码特征，共4232个，实际使用前1987个
oogle_ben_permission.csv ：验证实验提取的Google Play样本权限特征，共4232个，实际使用前1987个