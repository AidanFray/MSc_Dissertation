import React, { Component } from 'react';
import {Text, View, StyleSheet} from 'react-native';

const styles = StyleSheet.create({
    baseText: {
      fontFamily: 'Cochin',
      textAlign: 'left'
    },
    titleText: {
      fontSize: 20,
      fontWeight: 'bold',
      textAlign: 'center'
    },
  });

export default class ExperimentDescription extends Component {

    render() {
        return (
            <div>
                <View style={{margin: "30px"}}>
                    <Text style={styles.titleText}>
                        Experiment Description
                    </Text>

                    <Text style={styles.baseText}>
                        {'\n\n'}
                        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque vel ipsum placerat, laoreet lectus sit amet, pretium dolor. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Suspendisse molestie neque a urna elementum, id vehicula mauris porttitor. Integer tempor varius libero vel tristique. In quis neque luctus, elementum dolor eu, dictum leo. Morbi quis sollicitudin erat, in convallis tortor. Quisque a erat auctor, euismod lacus vel, facilisis quam. Donec in imperdiet elit. Phasellus convallis, nibh ac venenatis ultricies, diam quam fringilla odio, id commodo sapien tellus quis est.
                        {'\n\n'}
                        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque vel ipsum placerat, laoreet lectus sit amet, pretium dolor. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Suspendisse molestie neque a urna elementum, id vehicula mauris porttitor. Integer tempor varius libero vel tristique. In quis neque luctus, elementum dolor eu, dictum leo. Morbi quis sollicitudin erat, in convallis tortor. Quisque a erat auctor, euismod lacus vel, facilisis quam. Donec in imperdiet elit. Phasellus convallis, nibh ac venenatis ultricies, diam quam fringilla odio, id commodo sapien tellus quis est.
                        {'\n\n'}
                        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque vel ipsum placerat, laoreet lectus sit amet, pretium dolor. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Suspendisse molestie neque a urna elementum, id vehicula mauris porttitor. Integer tempor varius libero vel tristique. In quis neque luctus, elementum dolor eu, dictum leo. Morbi quis sollicitudin erat, in convallis tortor. Quisque a erat auctor, euismod lacus vel, facilisis quam. Donec in imperdiet elit. Phasellus convallis, nibh ac venenatis ultricies, diam quam fringilla odio, id commodo sapien tellus quis est.
                    </Text>
                </View>
            </div>
        )
    }
}

