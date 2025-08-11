using System.Collections;
using UnityEngine;
using UnityEngine.UI; // Needed for the Layout Element and LayoutRebuilder

public class UIManager : MonoBehaviour
{
	[SerializeField] private GameObject dialogPanel;

	// Reference to the Layout Element on DialogBoxPanel
	[SerializeField] private LayoutElement dialogLayoutElement; 

	[SerializeField] private Text messageText;
	[SerializeField] private Button closeButton;

	[SerializeField] private GameObject spinnerPanel;
	[SerializeField] private Image spinnerImage;

	// We'll use these to control the dialog's size
	[Header("Dialog Box Settings")]
	[SerializeField] private float maxScreenWidthPercentage = 0.8f; // 80%

	// A little extra padding for the preferred width calculation
	[SerializeField] private float horizontalPadding = 100f; 

	[Header("Loading Spinner Settings")]
	[SerializeField] private float spinSpeed = 100f;

	private Coroutine spinnerCoroutine;

	private void Start()
	{
		if (closeButton != null)
		{
			closeButton.onClick.AddListener(HideDialog);
		}
	}

	private void OnDestroy()
	{
		if (closeButton != null)
		{
			closeButton.onClick.RemoveListener(HideDialog);
		}
	}

	public void ShowDialog(string message)
	{
		// 1. Hide the spinner
		HideLoadingSpinner();

		// 2. Temporarily disable the Layout Element's preferred width setting
		// This allows the text to calculate its unconstrained width
		dialogLayoutElement.enabled = false;

 		// 3. Set the text of the message
		messageText.text = message;

		// 4. Get the width the text element would prefer based on its content
		// The Layout Element needs to be rebuilt to get the correct preferred width
		LayoutRebuilder.ForceRebuildLayoutImmediate(dialogLayoutElement.GetComponent<RectTransform>());

		float preferredTextWidth = messageText.preferredWidth;

		// 5. Calculate the maximum allowed width based on the screen size
		float maxAllowedWidth = Screen.width * maxScreenWidthPercentage;

		// 6. Apply the conditional logic
		if (preferredTextWidth + horizontalPadding > maxAllowedWidth)
		{
			// If the text is long, enable the Layout Element and set the width to the maximum
			dialogLayoutElement.enabled = true;
			dialogLayoutElement.preferredWidth = maxAllowedWidth;
		}
		else
		{
			// If the text is short, disable the Layout Element's preferred width
			// The Content Size Fitter will then take over and size it to the content
			dialogLayoutElement.enabled = false;
		}

		// 7. Ensure the UI updates before being shown
		// This is crucial for dynamic changes to take effect immediately
		LayoutRebuilder.ForceRebuildLayoutImmediate(dialogLayoutElement.GetComponent<RectTransform>());

		// 8. Show the dialog panel
		dialogPanel.SetActive(true);
	}

	public void HideDialog()
	{
		dialogPanel.SetActive(false);
	}

	public void ShowLoadingSpinner()
	{
		if (spinnerImage != null)
		{
			spinnerImage.fillAmount = 0;
			spinnerImage.fillClockwise = true;
		}

		if (spinnerCoroutine != null)
		{
			StopCoroutine(spinnerCoroutine);
			spinnerCoroutine = null;
		}

		spinnerCoroutine = StartCoroutine(LoadingSpinner());

		spinnerPanel.SetActive(true);
	}

	public void HideLoadingSpinner()
	{
		spinnerPanel.SetActive(false);

		if (spinnerCoroutine != null)
		{
			StopCoroutine(spinnerCoroutine);
			spinnerCoroutine = null;
		}
	}

	private IEnumerator LoadingSpinner()
	{
		if (spinnerImage != null)
		{
			while (true)
			{
				float speed = spinnerImage.fillClockwise ? spinSpeed : -spinSpeed;
				
				 // Increment the fill amount to create a spinning effect
				spinnerImage.fillAmount += speed * Time.deltaTime / 360f;

				// Loop the fill amount between 0 and 1
				if (spinnerImage.fillAmount <= 0f || spinnerImage.fillAmount >= 1f)
				{
					spinnerImage.fillClockwise = !spinnerImage.fillClockwise;
					spinnerImage.fillAmount = spinnerImage.fillClockwise ? 0f : 360f;
				}
				
				yield return null;
			}
		}
	}
}
