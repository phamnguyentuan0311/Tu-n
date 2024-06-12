from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from symspellpy import SymSpell

# Khai báo biến toàn cục
single_characters = set()
sym_spell = SymSpell()

def load_single_characters(filename="vietnam74K.txt"):
    global single_characters
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                word = line.strip().lower()
                single_characters.add(word)
    except Exception as e:
        print(f"Lỗi khi tải file {filename}: {e}")

def initialize_symspell():
    global sym_spell
    dictionary_path = 'dictionary.txt'
    bigram_dictionary_path = 'dictionary_bigram.txt'

    try:
        if not sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1, separator=' ', encoding='utf-8'):
            raise RuntimeError(f"Không thể tải file từ điển: {dictionary_path}")
        
        convert_bigram_dictionary(bigram_dictionary_path, 'converted_dictionary_bigram.txt')
        if not sym_spell.load_bigram_dictionary('converted_dictionary_bigram.txt', term_index=0, count_index=2, separator=' ', encoding='utf-8'):
            raise RuntimeError(f"Không thể tải file từ điển bigram: converted_dictionary_bigram.txt")
    except Exception as e:
        print(f"Lỗi khi khởi tạo SymSpell: {e}")

def convert_bigram_dictionary(input_filename, output_filename):
    with open(input_filename, 'r', encoding='utf-8') as input_file, \
         open(output_filename, 'w', encoding='utf-8') as output_file:
        for line in input_file:
            words, count = line.rsplit(' ', 1)
            output_file.write(f"{words}\t{count}")

def similarity_score(word1, word2, previous_word=None, next_word=None):
    vectorizer = CountVectorizer().fit_transform([word1, word2])
    vectors = vectorizer.toarray()
    csim = cosine_similarity(vectors)
    return csim[0,1]

def get_correct_text(word, previous_word=None, next_word=None):
    global sym_spell
    suggestions = []

    # Tạo chuỗi tìm kiếm dựa trên ngữ cảnh
    search_string = f"{previous_word} {word} {next_word}" if previous_word or next_word else word

    # Lấy đề xuất từ SymSpell
    suggestions = sym_spell.lookup_compound(search_string, max_edit_distance=2)

    if not suggestions:
        return word

    best_suggestion = None
    best_score = -1  # Khởi tạo điểm số tốt nhất là -1 để bất kỳ điểm số nào cũng lớn hơn

    for suggestion in suggestions:
        # Tính điểm độ tương đồng cosine
        context_similarity_score = similarity_score(word, suggestion.term, previous_word, next_word)

        # Tính điểm xác suất, tránh chia cho số 0
        probability_score = 1 / (suggestion.count + 1)

        # Tổng điểm = Điểm độ tương đồng + Điểm xác suất
        total_score = context_similarity_score + probability_score

        # Cập nhật đề xuất tốt nhất nếu tổng điểm cao hơn
        if total_score > best_score:
            best_suggestion = suggestion.term.split(' ')[1] if ' ' in suggestion.term else suggestion.term

    return best_suggestion if best_suggestion else word

def correct_text(text):
    global single_characters
    words = text.lower().split()
    corrected_text = []
    for i, word in enumerate(words):
        if word not in single_characters:
            previous_word = words[i - 1] if i > 0 else None
            next_word = words[i + 1] if i < len(words) - 1 else None
            correct_word = get_correct_text(word, previous_word, next_word)
            corrected_text.append(correct_word)
        else:
            corrected_text.append(word)
    return ' '.join(corrected_text)

# Khởi tạo và sử dụng các hàm
load_single_characters()
initialize_symspell()

def count_words(text):
    words = text.split()
    return len(words)
