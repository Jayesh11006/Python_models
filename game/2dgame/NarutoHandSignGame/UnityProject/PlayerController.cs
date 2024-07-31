using UnityEngine;

public class PlayerController : MonoBehaviour
{
    public float speed = 5.0f;

    void Update()
    {
        // Movement code here
    }

    public void PerformJutsu(string jutsu)
    {
        Debug.Log("Performing Jutsu: " + jutsu);
    }
}
