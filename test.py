import easyocr

reader = easyocr.Reader(["ch_sim", "en"], download_enabled=True)

# result = reader.readtext(r"d:\PytestAutoApi\test.jpg")

# print(result)
# print(result[0][1])

result2 = reader.readtext(r"d:\PytestAutoApi\login_success.png", detail=0)
print(result2)
print(",".join(result2))