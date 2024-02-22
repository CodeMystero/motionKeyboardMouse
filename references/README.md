예외 무시

잘못 프로그래밍된 프로그램은 제어하기 힘든 상황이 발생할 수 있다. 때문에 pyautogui에서는 기본적으로 마우스 커서가 (0,0) 위치로 이동하면 자동으로 프로그램이 종료되게 설정되어 있다. 해당 기능을 끄고 싶다면 다음을 설정하길 바란다.

```python
import pyautogui
pyautogui.FAILSAFE = False
```
