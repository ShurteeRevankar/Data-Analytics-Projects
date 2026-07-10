from utils.prediction import predict_business


result = predict_business(

    category="Restaurant",

    city="Panvel",

    rating=4.7,

    reviews=500,

    website="No"

)


print(result)