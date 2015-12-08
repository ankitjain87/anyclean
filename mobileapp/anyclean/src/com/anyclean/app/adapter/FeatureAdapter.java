package com.anyclean.app.adapter;

import java.util.List;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.TextView;

import com.anyclean.app.R;

public class FeatureAdapter extends ArrayAdapter<Feature> {

	final private Context context;
	final private List<Feature> features;

	public FeatureAdapter(Context context, int resource, List<Feature> objects) {
		super(context, resource, objects);
		this.context = context;
		this.features = objects;
	}

	@Override
	public View getView(int position, View convertView, ViewGroup parent) {
		LayoutInflater inflater = (LayoutInflater) context
				.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
		View rowView = inflater.inflate(R.layout.feature_list_item, parent,
				false);
		Feature feature = features.get(position);
		TextView textView = (TextView) rowView
				.findViewById(R.id.linearLayout_textview1_feature_item);
		textView.setText(feature.getFeature());
		return rowView;
	}
}
