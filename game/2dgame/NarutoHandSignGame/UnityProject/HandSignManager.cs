using System.Collections;
using UnityEngine;
using UnityEngine.Networking;

public class HandSignManager : MonoBehaviour
{
    public PlayerController player;

    IEnumerator CaptureAndSend()
    {
        yield return new WaitForEndOfFrame();
        Texture2D screenImage = new Texture2D(Screen.width, Screen.height);
        screenImage.ReadPixels(new Rect(0, 0, Screen.width, Screen.height), 0, 0);
        screenImage.Apply();
        byte[] imageBytes = screenImage.EncodeToJPG();

        WWWForm form = new WWWForm();
        form.AddBinaryData("image", imageBytes, "image.jpg", "image/jpeg");

        UnityWebRequest www = UnityWebRequest.Post("http://localhost:5000/detect", form);
        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success)
        {
            Debug.Log(www.error);
        }
        else
        {
            string jutsu = www.downloadHandler.text;
            player.PerformJutsu(jutsu);
        }
    }

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Space))
        {
            StartCoroutine(CaptureAndSend());
        }
    }
}
