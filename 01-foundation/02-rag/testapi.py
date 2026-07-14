from openai import OpenAI, AuthenticationError

# 1. Add your list of keys here
api_keys = [

]

print(f"{'KEY (Masked)':<20} | {'STATUS':<10} | {'RPM LIMIT':<10} | {'TIER ESTIMATE'}")
print("-" * 70)

for key in api_keys:
    # Mask the key for display (show only first 4 and last 4 chars)
    masked_key = f"{key[:4]}...{key[-4:]}"
    
    try:
        # Initialize client with the specific key
        client = OpenAI(api_key=key)
        
        # Make a cheap 1-token request and get RAW response to see headers
        response = client.chat.completions.with_raw_response.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Hi"}],
            max_tokens=1
        )
        
        # Extract the Request Per Minute (RPM) limit from headers
        rpm = int(response.headers.get('x-ratelimit-limit-requests', 0))
        
        # Estimate Tier based on RPM (Approximate values)
        # Tier 1 (Paid) usually starts around 3,500+ RPM for standard models
        # Free tier is usually much lower (e.g. 3 RPM or similar restrictions)
        if rpm < 500:
            tier = "Free/Trial"
        elif rpm < 5000:
            tier = "Tier 1 (Paid)"
        else:
            tier = "Tier 2+ (High)"

        print(f"{masked_key:<20} | {'VALID':<10} | {rpm:<10} | {tier}")

    except AuthenticationError:
        print(f"{masked_key:<20} | {'INVALID':<10} | {'N/A':<10} | {'N/A'}")
    except Exception as e:
        print(f"{masked_key:<20} | {'ERROR':<10} | {'N/A':<10} | {str(e)[:20]}")
