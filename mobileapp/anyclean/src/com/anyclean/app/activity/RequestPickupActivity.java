package com.anyclean.app.activity;

import com.anyclean.app.R;

import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.EditText;

public class RequestPickupActivity extends ActionBarActivity {

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		// getApplicationContext().startService(new Intent(this,
		// FirstHttpCallIntentServeice.class));
		setContentView(R.layout.activity_request_pickup);
	}

	@Override
	protected void onResume() {
		super.onResume();

		Button registerButton = (Button) this
				.findViewById(R.id.linearLayout_button1_register);

		EditText userNameEditText = (EditText) this
				.findViewById(R.id.linearLayout_edittext1_name);

		EditText emailEditText = (EditText) this
				.findViewById(R.id.linearLayout_edittext2_email);

		EditText mobileEditText = (EditText) this
				.findViewById(R.id.linearLayout_edittext3_mobile);

		EditText passwordEditText = (EditText) this
				.findViewById(R.id.linearLayout_edittext4_password);

		EditText rePasswordEditText = (EditText) this
				.findViewById(R.id.linearLayout_edittext5_re_password);

		registerButton.setOnClickListener(clickListener);

	}

	OnClickListener clickListener = new OnClickListener() {

		@Override
		public void onClick(final View v) {
			switch (v.getId()) {
			case R.id.linearLayout_button1_register:
				// perform validation and register
				break;
			default:
				Log.d("", "");
			}
		}
	};

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.main, menu);
		return true;
	}

	@Override
	public boolean onOptionsItemSelected(MenuItem item) {
		// Handle action bar item clicks here. The action bar will
		// automatically handle clicks on the Home/Up button, so long
		// as you specify a parent activity in AndroidManifest.xml.
		int id = item.getItemId();
		if (id == R.id.action_settings) {
			return true;
		}
		return super.onOptionsItemSelected(item);
	}

}
