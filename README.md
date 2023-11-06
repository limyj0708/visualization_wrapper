# Modules_for_work
- 업무를 하다 보면 반복적으로 작성되는 코드들이 있습니다.
- 특히 데이터 시각화 코드가 그렇습니다.
- 코드를 재사용하려면 예전에 작성한 노트북에 가서 코드를 긁어 와야 합니다. 3주 이상 시간이 흐른 후라면, 어느 파일에서 해당 코드를 작성했었는지도 가물가물해집니다. 한 달 이상 시간이 지나면, 어떻게 작성했었는지도 조금씩 잊기 시작합니다!
- Repo에 저장해 두고, 노트북에서 아래처럼 불러와서 사용하면 되겠다는 결론에 도달했습니다.
```Python
import requests
request = request.get("https://raw.githbusercontent.com/username/repo/square.py")
with open("square.py", "wb") as f:
  f.write(request.content)

from square import return_square
```
