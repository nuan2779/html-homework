from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="../frontend"), name="static")

def predict_price(area: float, bedrooms: int, location: str) -> float:
    base_price = 500_000_000 # Base price in vnd
    price_per_sq_meter = 15_000_000
    price_per_bedroom = 50_000_000
    total_price = base_price + (area * price_per_sq_meter) + (bedrooms * price_per_bedroom)

    location = location.lower()
    if location == "hanoi":
        total_price *= 1.3
    if location == "hcmc":
        total_price *= 1.25
    final_price = round(total_price, -6)
    return float(final_price)

@app.get("/predict")
def get_prediction(area: float, bedrooms: int, location: str = "other"):
#Dùng def là bởi vì việc dự đoán giá là một hành động đồng bộ, không có độ trễ như việc truy vấn database hay gọi API bên ngoài, 
#tối ưu thời gian chạy trên cpu
    price = predict_price(area, bedrooms, location)
    return {"area": area,
            "bedrooms": bedrooms,
            "location": location,
            "predicted_price": price}

#Nếu không có location lúc điền form thì vẫn chạy được thì trong hàm để là location: str = "other" , việc này giúp fastapi hiểu rằng nếu không có location thì mặc định là "other" và vẫn chạy được, tránh lỗi khi người dùng không nhập location
#Nếu không có area thì sẽ báo lỗi vì area là bắt buộc, nếu muốn area không bắt buộc thì có thể để là area: float = 0.0, nếu để bình thường thì area không có giá trịnh mặc định nên fastapi sẽ báo lỗi khi không có area, nếu muốn area không bắt buộc thì có thể để là area: float = 0.0, nếu để bình thường thì area không có giá trị mặc định nên fastapi sẽ báo lỗi khi không có area